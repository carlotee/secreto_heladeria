proyecto backend basado en un proyecto real de una heladeria, y se nos asigno el area de costo asi que todo esta en base al area de costo, se le agrega seguridad 
por token igual

se ocuparon las tecnologias que son Como Backend y Frontend se ocupo Django, y como motor de base de datos MySQl

---------------------------------------------------------------------------------------------------------------------
cargar semilla para cada app (proveedor y produccion)

python manage.py loaddata proveedores/fixtures/proveedores.json
python manage.py loaddata produccion/fixtures/productos.json

--------------------------------------------------------------------------------------------------------------------------

para ocupar las dependecias 
pip install -r requirements.txt


Restaurar dependencias en otro entorno Si en otro PC (o servidor) clonas tu proyecto, solo haces
pip install -r requirements.txt

cada vez que instalas una nueva libreria actualizar el archivo requirements.txt para asi tenerlo al dia
pip freeze > requirements.txt



Admin
12345

contraseña compus de Incapaz: admin
