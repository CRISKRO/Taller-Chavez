from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from usuarios.models import UsuarioPersonalizado
from clientes.models import Cliente, Vehiculo
from inventario.models import Categoria, ArticuloInventario
from ordenes.models import OrdenServicio, RefaccionOrden
from facturacion.models import Factura
from usuarios.forms import UsuarioForm

class TallerChavezQATestMatrix(TestCase):
    """
    Suite de Pruebas Automatizadas de Control de Calidad (QA)
    según la Matriz de Casos de Prueba del Manual Chávez WorkShop Manager.
    """

    def setUp(self):
        # Crear usuarios con diferentes roles
        self.admin_user = UsuarioPersonalizado.objects.create_user(
            username='admin_test',
            password='Password123',
            rol='ADMIN',
            first_name='Admin',
            last_name='General'
        )
        self.recepcionista_user = UsuarioPersonalizado.objects.create_user(
            username='recep_test',
            password='Password123',
            rol='RECEPCIONISTA',
            first_name='Laura',
            last_name='Recepción'
        )
        self.mecanico_user = UsuarioPersonalizado.objects.create_user(
            username='meca_test',
            password='Password123',
            rol='MECANICO',
            first_name='Carlos',
            last_name='Taller'
        )
        self.mecanico_otro = UsuarioPersonalizado.objects.create_user(
            username='meca_otro',
            password='Password123',
            rol='MECANICO',
            first_name='Luis',
            last_name='Piso'
        )

        # Crear cliente y vehículo base
        self.cliente = Cliente.objects.create(
            nombre='Juan Pérez',
            email='juan@example.com',
            telefono='555-1234'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente,
            marca='Toyota',
            modelo='Corolla',
            anio=2021,
            color='Rojo Cereza',
            placa='ABC-123',
            vin='3N1AB7AP4HY123456',
            kilometraje=45000
        )

        # Crear inventario base
        self.categoria = Categoria.objects.create(nombre='Frenos')
        self.articulo_balatas = ArticuloInventario.objects.create(
            codigo='BAL-001',
            nombre='Juego de Balatas Delanteras',
            categoria=self.categoria,
            stock_actual=10,
            stock_minimo=3,
            precio_unitario=Decimal('650.00')
        )
        self.articulo_liquido = ArticuloInventario.objects.create(
            codigo='LIQ-002',
            nombre='Líquido de Frenos DOT4',
            categoria=self.categoria,
            stock_actual=15,
            stock_minimo=5,
            precio_unitario=Decimal('150.00')
        )

    # -------------------------------------------------------------
    # TC-AUT-01: Autenticación - Inicio con credenciales válidas
    # -------------------------------------------------------------
    def test_tc_aut_01_login_redirection(self):
        client = Client()
        # Login de Mecánico -> Redirección a su Bandeja Técnica
        response_meca = client.post(reverse('login'), {
            'username': 'meca_test',
            'password': 'Password123'
        }, follow=True)
        self.assertEqual(response_meca.status_code, 200)
        self.assertRedirects(response_meca, reverse('ordenes_bandeja'))
        client.logout()

        # Login de Recepcionista -> Redirección a Dashboard
        response_recep = client.post(reverse('login'), {
            'username': 'recep_test',
            'password': 'Password123'
        }, follow=True)
        self.assertEqual(response_recep.status_code, 200)
        self.assertRedirects(response_recep, reverse('dashboard'))

    # -------------------------------------------------------------
    # TC-AUT-02: Autenticación - Contraseña incorrecta
    # -------------------------------------------------------------
    def test_tc_aut_02_invalid_credentials(self):
        client = Client()
        response = client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'WrongPassword999'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        # Debe permanecer en login y contener mensaje de error
        self.assertContains(response, 'Credenciales inválidas')

    # -------------------------------------------------------------
    # TC-USR-01: Usuarios - Contraseña menor a 8 caracteres
    # -------------------------------------------------------------
    def test_tc_usr_01_password_length_validation(self):
        # Intentar crear un usuario con contraseña de 5 caracteres
        form_data = {
            'username': 'nuevo_usuario',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'rol': 'MECANICO',
            'telefono': '555-0000',
            'password': '12345' # Menor a 8 caracteres
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('al menos 8 caracteres', form.errors['password'][0])

        # Con contraseña válida (>= 8 caracteres)
        form_data['password'] = 'ClaveSegura123'
        form_valid = UsuarioForm(data=form_data)
        self.assertTrue(form_valid.is_valid())

    # -------------------------------------------------------------
    # TC-USR-02: Seguridad - Mecánico accede a Facturación (Quality Gate 403)
    # -------------------------------------------------------------
    def test_tc_usr_02_mechanic_denied_billing_403(self):
        client = Client()
        client.login(username='meca_test', password='Password123')

        # Intento de acceso a facturación
        response_facturacion = client.get(reverse('facturacion_lista'))
        self.assertEqual(response_facturacion.status_code, 403)

        # Intento de acceso a administración de usuarios
        response_usuarios = client.get(reverse('usuarios_lista'))
        self.assertEqual(response_usuarios.status_code, 403)

    # -------------------------------------------------------------
    # TC-CLI-01: Clientes - Registro con VIN y Color
    # -------------------------------------------------------------
    def test_tc_cli_01_vehicle_vin_color_persistence(self):
        vehiculo_nuevo = Vehiculo.objects.create(
            cliente=self.cliente,
            marca='Honda',
            modelo='Civic',
            anio=2022,
            color='Azul Noche',
            placa='XYZ-789',
            vin='1HGCR2F83HA001122',
            kilometraje=32000
        )
        # Verificar persistencia en base de datos
        db_vehiculo = Vehiculo.objects.get(placa='XYZ-789')
        self.assertEqual(db_vehiculo.color, 'Azul Noche')
        self.assertEqual(db_vehiculo.vin, '1HGCR2F83HA001122')
        self.assertEqual(db_vehiculo.cliente, self.cliente)

    # -------------------------------------------------------------
    # TC-ORD-01: Órdenes - Asignación de mecánico y visibilidad en bandeja
    # -------------------------------------------------------------
    def test_tc_ord_01_mechanic_inbox_visibility(self):
        orden_carlos = OrdenServicio.objects.create(
            numero='101',
            cliente=self.cliente,
            vehiculo=self.vehiculo,
            mecanico=self.mecanico_user,
            estado='RECIBIDO',
            descripcion='Revisión de frenos y suspensión'
        )
        orden_luis = OrdenServicio.objects.create(
            numero='102',
            cliente=self.cliente,
            vehiculo=self.vehiculo,
            mecanico=self.mecanico_otro,
            estado='RECIBIDO',
            descripcion='Cambio de aceite y filtros'
        )

        client = Client()
        client.login(username='meca_test', password='Password123')
        response = client.get(reverse('ordenes_bandeja'))
        self.assertEqual(response.status_code, 200)
        # La OT de Carlos debe aparecer, pero la de Luis no
        self.assertContains(response, 'OT-101')
        self.assertNotContains(response, 'OT-102')

    # -------------------------------------------------------------
    # TC-ORD-02: Órdenes - Salto "Pendiente" a "Concluido" bloqueado
    # -------------------------------------------------------------
    def test_tc_ord_02_invalid_state_jump_blocked(self):
        orden = OrdenServicio.objects.create(
            numero='201',
            cliente=self.cliente,
            vehiculo=self.vehiculo,
            mecanico=self.mecanico_user,
            estado='RECIBIDO',
            descripcion='Falla en encendido'
        )

        client = Client()
        client.login(username='admin_test', password='Password123')

        # Intentar forzar salto directo de RECIBIDO a CONCLUIDO
        response = client.post(reverse('orden_cambiar_estado', args=[orden.id]), {
            'nuevo_estado': 'CONCLUIDO'
        }, follow=True)

        orden.refresh_from_db()
        # El estado NO debe haber cambiado a CONCLUIDO
        self.assertEqual(orden.estado, 'RECIBIDO')
        self.assertContains(response, 'Violación de Quality Gate')

        # Intentar pasar a CONCLUIDO desde EN_PROCESO sin diagnóstico
        orden.estado = 'EN_PROCESO'
        orden.diagnostico = ''
        orden.save()

        response_sin_diag = client.post(reverse('orden_cambiar_estado', args=[orden.id]), {
            'nuevo_estado': 'CONCLUIDO'
        }, follow=True)

        orden.refresh_from_db()
        self.assertEqual(orden.estado, 'EN_PROCESO')
        self.assertContains(response_sin_diag, 'sin haber registrado previamente el Diagnóstico Técnico')

    # -------------------------------------------------------------
    # TC-INV-01: Inventario - Descuento atómico al cerrar OT
    # -------------------------------------------------------------
    def test_tc_inv_01_atomic_stock_deduction_on_complete(self):
        orden = OrdenServicio.objects.create(
            numero='301',
            cliente=self.cliente,
            vehiculo=self.vehiculo,
            mecanico=self.mecanico_user,
            estado='EN_PROCESO',
            descripcion='Cambio de balatas y líquido',
            diagnostico='Balatas gastadas al 90% y líquido contaminado.'
        )
        # Añadir refacciones a la orden
        RefaccionOrden.objects.create(
            orden=orden,
            articulo=self.articulo_balatas,
            cantidad=2, # Requiere 2 juegos
            precio_unitario=Decimal('650.00')
        )
        RefaccionOrden.objects.create(
            orden=orden,
            articulo=self.articulo_liquido,
            cantidad=1, # Requiere 1 bote
            precio_unitario=Decimal('150.00')
        )

        stock_balatas_inicial = self.articulo_balatas.stock_actual # 10
        stock_liquido_inicial = self.articulo_liquido.stock_actual # 15

        client = Client()
        client.login(username='admin_test', password='Password123')

        # Concluir la orden
        response = client.post(reverse('orden_cambiar_estado', args=[orden.id]), {
            'nuevo_estado': 'CONCLUIDO'
        }, follow=True)

        orden.refresh_from_db()
        self.assertEqual(orden.estado, 'CONCLUIDO')
        self.assertTrue(orden.inventario_descontado)

        # Validar actualización atómica de stock en DB
        self.articulo_balatas.refresh_from_db()
        self.articulo_liquido.refresh_from_db()
        self.assertEqual(self.articulo_balatas.stock_actual, stock_balatas_inicial - 2) # 8
        self.assertEqual(self.articulo_liquido.stock_actual, stock_liquido_inicial - 1) # 14

    # -------------------------------------------------------------
    # TC-FAC-01: Facturación - Cálculo total con Anticipos y Bloqueo de PDF
    # -------------------------------------------------------------
    def test_tc_fac_01_billing_calculation_with_advances_and_pdf_gate(self):
        orden = OrdenServicio.objects.create(
            numero='401',
            cliente=self.cliente,
            vehiculo=self.vehiculo,
            mecanico=self.mecanico_user,
            estado='CONCLUIDO',
            descripcion='Servicio mayor de frenos',
            diagnostico='Reemplazo integral completado.',
            mano_de_obra=Decimal('800.00'),
            anticipo=Decimal('500.00'), # Anticipo dejado
            inventario_descontado=True
        )
        RefaccionOrden.objects.create(
            orden=orden,
            articulo=self.articulo_balatas,
            cantidad=1,
            precio_unitario=Decimal('650.00')
        )

        # Generar Factura
        factura = Factura.objects.create(
            orden=orden,
            metodo_pago='TRANSFERENCIA',
            estado='PENDIENTE'
        )

        # Subtotal = Mano de Obra (800) + Refacciones (650) = 1450.00
        self.assertEqual(factura.subtotal, Decimal('1450.00'))
        # IVA (16%) = 1450 * 0.16 = 232.00
        self.assertEqual(factura.iva, Decimal('232.00'))
        # Total = 1450 + 232 = 1682.00
        self.assertEqual(factura.total, Decimal('1682.00'))
        # Anticipo aplicado = 500.00
        self.assertEqual(factura.anticipo_aplicado, Decimal('500.00'))
        # Saldo a liquidar = 1682 - 500 = 1182.00
        self.assertEqual(factura.saldo_pendiente, Decimal('1182.00'))

        client = Client()
        client.login(username='recep_test', password='Password123')

        # Intento de descargar PDF cuando la factura está PENDIENTE -> Bloqueado
        response_pdf_bloqueado = client.get(reverse('generar_pdf_factura', args=[factura.id]), follow=True)
        self.assertContains(response_pdf_bloqueado, 'Quality Gate Financiero')

        # Liquidar factura / registrar pago
        factura.estado = 'PAGADO'
        factura.save()

        # Descarga de PDF cuando está PAGADA -> PDF liberado con HTTP 200 application/pdf
        response_pdf_liberado = client.get(reverse('generar_pdf_factura', args=[factura.id]))
        self.assertEqual(response_pdf_liberado.status_code, 200)
        self.assertEqual(response_pdf_liberado['Content-Type'], 'application/pdf')
