cargar semilla para cada app (proveedor y produccion)

python manage.py loaddata proveedores/fixtures/proveedores.json
python manage.py loaddata produccion/fixtures/productos.json

----------------------------------------

User_limitado
user_limited@gmail.com
User_bajo123

usuarios limitados y admin

admin
admin@gmail.com
admin123

----------------------------------------

para ocupar las dependecias 
pip install -r requirements.txt


Restaurar dependencias en otro entorno Si en otro PC (o servidor) clonas tu proyecto, solo haces
pip install -r requirements.txt

cada vez que instalas una nueva libreria actualizar el archivo requirements.txt para asi tenerlo al dia
pip freeze > requirements.txt


-------------------------------------------------------
⚙️ 1. Admin Básico (10 pts)

Modelos registrados:

accounts: Usuario, Registro

proveedores: Proveedor

produccion: Producto, Costo

centro_costos: Periodo, TipoCosto, Centro_Costos, Costo

Personalización aplicada:

Columnas (list_display)

Búsqueda (search_fields)

Filtros (list_filter)

Orden (ordering)

📍 Ubicación:

accounts/admin.py

proveedores/admin.py

produccion/admin.py

centro_costos/admin.py
-----------------------------------------------------------------------------------------
🧩 2. Admin Pro (22 pts)

A) Inline – Productos dentro de Proveedores
📍 proveedores/admin.py
Permite administrar productos directamente desde el formulario de proveedores.

B) Acción personalizada – Borrado lógico de Costos
📍 produccion/admin.py
Acción en el admin que marca los costos con deleted_at sin eliminarlos físicamente.

C) Validación – Valor de Costo > 0
📍 produccion/forms.py
Valida que el valor del costo sea mayor que cero antes de guardarlo.

Admin
12345

contraseña compus de Incapaz: admin