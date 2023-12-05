from flask import Flask,render_template,request,redirect,url_for,jsonify
import cx_Oracle

app = Flask(__name__)

def obtenerDatos(query):
    connection = cx_Oracle.connect("USERDB", "PASSWORD", dsn)

    cursor = connection.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()
    return resultados

def ejecutarProcedure(procedure,parametros):
    try:
        connection = cx_Oracle.connect("USERDB", "PASSWORD", dsn)
        cursor = connection.cursor()
        cursor.callproc(procedure, parametros)
        cursor.close()
        connection.commit()
        connection.close()
    except cx_Oracle.Error as error:
        print(f"Error en ejecutarProcedure: {error}")

def ejecutarFuncion(funcion,parametro,siP,output):
    try:
        connection = cx_Oracle.connect("USERDB", "PASSWORD", dsn)
        cursor = connection.cursor()
        if siP:
            if output == "string":
                valor = cursor.callfunc(funcion,cx_Oracle.STRING,parametro)
            elif output == "int":
                valor = cursor.callfunc(funcion,cx_Oracle.NUMBER,parametro)
        else:
            if output == "string":
                valor = cursor.callfunc(funcion,cx_Oracle.STRING)
            elif output == "int":
                valor = cursor.callfunc(funcion,cx_Oracle.NUMBER)
        cursor.close()
        connection.close()
        print("Se ejecuto la funcion")
        return valor
    except cx_Oracle.Error as error:
        print(f"Error en ejecutarProcedure: {error}")

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/Productos')
def productos():
    query = "SELECT P.ID_PRODUCTO,P.NOMBRE,P.TIPO,P.STOCK,P.PRECIO,P.TALLA,P.COLOR,PE.NOMBRE FROM PRODUCTO P LEFT JOIN VENDEDOR V ON P.ID_VENDEDOR = V.ID_VENDEDOR JOIN PERSONA PE ON PE.DNI = V.DNI ORDER BY P.ID_PRODUCTO"
    datos = obtenerDatos(query)
    return render_template('productos.html',resultados=datos)

@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    idProducto = request.form.get('idRProducto')
    nombre = request.form.get('RNombre')
    tipo = request.form.get('RTipo')
    stock = request.form.get('RStock')
    precio = request.form.get('RPrecio')
    talla = request.form.get('RTalla')
    color = request.form.get('RColor')
    vendedor = request.form.get('RNombreVendedor')

    parametros = (idProducto,nombre,tipo,stock,precio,talla,color,vendedor)
    ejecutarProcedure('InsertarProducto', parametros)
    print("Se añadio el producto")
    return redirect('/Productos')

@app.route('/eliminarProducto',methods=['POST'])
def eliminarProducto():
    idProducto = request.form.get('DidProducto')
    parametros = (idProducto,)
    ejecutarProcedure('EliminarProducto',parametros)
    print("Se elimino el producto")
    return redirect('/Productos')

@app.route('/Vendedores')
def vendedores():
    query = "SELECT V.ID_VENDEDOR,V.DNI,P.NOMBRE,P.APELLIDOPATERNO,P.APELLIDOMATERNO,P.TELEFONO FROM VENDEDOR V JOIN PERSONA P ON P.DNI = V.DNI ORDER BY V.ID_VENDEDOR"
    datos = obtenerDatos(query)
    return render_template('vendedores.html',resultados=datos)

@app.route('/agregarVendedor', methods=['POST'])
def agregarVendedor():
    idVendedor = request.form.get('idVendedor')
    dni = request.form.get('Vdni')
    nombre = request.form.get('VNombre')
    apellidoPat = request.form.get('VApellidoPat')
    apellidoMat = request.form.get('VApellidoMat')
    telefono = request.form.get('VTelefono')

    parametros = (idVendedor, dni, nombre, apellidoPat, apellidoMat, telefono)
    ejecutarProcedure('CrearVendedor', parametros)
    print("Se añadio el vendedor")
    return redirect('/Vendedores')

@app.route('/eliminarVendedor',methods=['POST'])
def eliminarVendedor():
    idVendedor = request.form.get('idDVendedor')
    dni = request.form.get('dniD')
    parametros = (idVendedor,dni)
    ejecutarProcedure('EliminarVendedor',parametros)
    print("Se elimino el vendedor")
    return redirect('/Vendedores')

@app.route('/Clientes')
def clientes():
    query = "SELECT C.ID_CLIENTE,C.DNI,P.NOMBRE,P.APELLIDOPATERNO,P.APELLIDOMATERNO,P.TELEFONO FROM CLIENTE C JOIN PERSONA P ON P.DNI = C.DNI ORDER BY C.ID_CLIENTE"
    datos = obtenerDatos(query)
    return render_template('clientes.html',resultados=datos)

@app.route('/agregarCliente', methods=['POST'])
def agregarCliente():
    idCliente = request.form.get('idCliente')
    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    apellidoPat = request.form.get('apellidoPat')
    apellidoMat = request.form.get('apellidoMat')
    telefono = request.form.get('telefono')

    parametros = (idCliente, dni, nombre, apellidoPat, apellidoMat, telefono)
    ejecutarProcedure('CrearCliente', parametros)
    print("Se añadio el cliente")
    return redirect('/Clientes')

@app.route('/eliminarCliente',methods=['POST'])
def eliminarCliente():
    idCliente = request.form.get('idClienteD')
    dni = request.form.get('dniD')
    parametros = (idCliente,dni)
    ejecutarProcedure('EliminarCliente',parametros)
    print("Se elimino el cliente")
    return redirect('/Clientes')

@app.route('/Empleados')
def empleados():
    query = "SELECT E.ID_EMPLEADO,E.DNI,P.NOMBRE,P.APELLIDOPATERNO,P.APELLIDOMATERNO,P.TELEFONO,E.SALARIO FROM EMPLEADO E JOIN PERSONA P ON P.DNI = E.DNI ORDER BY E.ID_EMPLEADO"
    datos = obtenerDatos(query)
    return render_template('empleados.html',resultados=datos)

@app.route('/agregarEmpleado', methods=['POST'])
def agregarEmpleado():
    idEmpleado = request.form.get('idEEmpleado')
    dni = request.form.get('Edni')
    nombre = request.form.get('ENombre')
    apellidoPat = request.form.get('EApellidoPat')
    apellidoMat = request.form.get('EApellidoMat')
    telefono = request.form.get('ETelefono')
    salario = 50000

    parametros = (idEmpleado, dni, nombre, apellidoPat, apellidoMat, telefono,salario)
    ejecutarProcedure('CrearEmpleado', parametros)
    print("Se añadio el empleado")
    return redirect('/Empleados')

@app.route('/eliminarEmpleado',methods=['POST'])
def eliminarEmpleado():
    idEmpleado = request.form.get('idEmpleadoD')
    dni = request.form.get('dniD')
    parametros = (idEmpleado,dni)
    ejecutarProcedure('EliminarEmpleado',parametros)
    print("Se elimino el empleado")
    return redirect('/Empleados')

@app.route('/Notificaciones')
def notificaciones():
    query = "SELECT N.ID_NOTIFICACION,N.TIPO,N.DESCRIPCION,PE.ID_PEDIDO,P_EMP.NOMBRE AS \"Nombre Empleado\",P_VEN.NOMBRE AS \"Nombre Vendedor\",PA.ID_PAGO FROM NOTIFICACION N JOIN PEDIDO PE ON PE.ID_PEDIDO = N.ID_PEDIDO JOIN PAGO PA ON PA.ID_PAGO = N.ID_PAGO LEFT JOIN EMPLEADO E ON E.ID_EMPLEADO = N.ID_EMPLEADO LEFT JOIN VENDEDOR V ON V.ID_VENDEDOR = N.ID_VENDEDOR JOIN PERSONA P_EMP ON P_EMP.DNI = E.DNI JOIN PERSONA P_VEN ON P_VEN.DNI = V.DNI ORDER BY N.ID_NOTIFICACION"
    datos = obtenerDatos(query)
    return render_template('notificaciones.html',resultados=datos)

@app.route('/agregarNotificacion', methods=['POST'])
def agregarNotificacion():
    idNoti = request.form.get('idENotificacion')
    tipo = request.form.get('NTipo')
    descripcion = request.form.get('NDescripcion')
    idPedido = request.form.get('NidPedido')
    NombreEmp = request.form.get('NNombreEmp')
    NombreVend = request.form.get('NNombreVend')
    idPago = request.form.get('NidPago')

    parametros = (idNoti,tipo,descripcion,idPedido,NombreEmp,NombreVend,idPago)
    ejecutarProcedure('RegistrarNotificacion', parametros)
    print("Se añadio la notificacion")
    return redirect('/Notificaciones')

@app.route('/eliminarNotificacion',methods=['POST'])
def eliminarNotificaciones():
    idNoti = request.form.get('idDNotificacion')
    parametros = (idNoti,)
    ejecutarProcedure('EliminarNotificacion',parametros)
    print("Se elimino la notificacion")
    return redirect('/Notificaciones')

@app.route('/Pedidos')
def pedidos():
    query = "SELECT PE.ID_PEDIDO,PE.MONTO,PE.DESCRIPCION,PE.CANTIDAD,P.NOMBRE,PR.NOMBRE FROM PEDIDO PE LEFT JOIN CLIENTE C ON C.ID_CLIENTE = PE.ID_CLIENTE JOIN PERSONA P ON P.DNI = C.DNI JOIN PRODUCTO PR ON PR.ID_PRODUCTO = PE.ID_PRODUCTO ORDER BY PE.ID_PEDIDO"
    datos = obtenerDatos(query)
    print(datos)    
    return render_template('pedidos.html',resultados=datos)

@app.route('/agregarPedido', methods=['POST'])
def agregarPedido():
    idPedido = request.form.get('idPedido')
    descripcion = request.form.get('PDescripcion')
    cantidad = request.form.get('PCantidad')
    NombreClient = request.form.get('PNombreClient')
    NombreProd = request.form.get('PNombreProd')

    parametros = (idPedido,descripcion,cantidad,NombreClient,NombreProd)
    ejecutarProcedure('RegistrarPedido', parametros)
    print("Se añadio el pedido")
    return redirect('/Pedidos')

@app.route('/eliminarPedido',methods=['POST'])
def eliminarPedido():
    idPedido = request.form.get('idDPedido')
    parametros = (idPedido,)
    ejecutarProcedure('EliminarPedido',parametros)
    print("Se elimino el pedido")
    return redirect('/Pedidos')

@app.route('/Pagos')
def pagos():
    query = "SELECT PA.ID_PAGO, PA.MONTO, PA.FECHAPAGO, PA.ESTADO, P.NOMBRE AS \"Cliente emisor\", PA.ID_PEDIDO FROM PAGO PA LEFT JOIN CLIENTE C ON C.ID_CLIENTE = PA.ID_CLIENTE JOIN PERSONA P ON P.DNI = C.DNI ORDER BY PA.ID_PAGO"
    datos = obtenerDatos(query)
    return render_template('pagos.html',resultados=datos)

@app.route('/agregarPago', methods=['POST'])
def agregarPago():
    idPago = request.form.get('idPPago')
    monto = request.form.get('PMonto')
    fechaPago = request.form.get('PFechaPago')
    estado = request.form.get('PEstado')
    NombreClient = request.form.get('PNombreClient')
    idPedido = request.form.get('PidPedido')

    parametros = (idPago,monto,str(fechaPago),estado,NombreClient,idPedido)
    ejecutarProcedure('RegistrarPago', parametros)
    print("Se añadio el pago")
    return redirect('/Pagos')

@app.route('/eliminarPago',methods=['POST'])
def eliminarPago():
    idPago = request.form.get('idDPago')
    parametros = (idPago,)
    ejecutarProcedure('EliminarPago',parametros)
    print("Se elimino el pago")
    return redirect('/Pagos')

@app.route('/Informacion')
def info():
    return render_template('informacion.html')

@app.route('/PagosTotales',methods=['POST'])
def PagosTotales():
    id_pago = request.form.get('idPago')
        # Llama a la función que interactúa con Oracle y obtiene el resultado
    resultado = ejecutarFuncion('CalcularTotalPagoCliente',(id_pago,),True,"int")
    print("Se obtuvieron los pagos totales del cliente: ",resultado)
    return jsonify({'result': resultado}), 200, {'Content-Type': 'application/json'}

@app.route('/ObtenerDescr',methods=['POST'])
def ObtenerDescr():
    idNoti = request.form.get('idNotificacion')
    resultado = ejecutarFuncion('ObtenerDescripcionNotificacion',(idNoti,),True,"string")
    print("Se obtuvo la descripción: ",resultado)
    return jsonify({'result': resultado}), 200, {'Content-Type': 'application/json'}

@app.route('/ContarEmp',methods=['POST'])
def ContarEmp():
    parametros = ()
    resultado = ejecutarFuncion('ContarEmpleados',parametros,False,"int")
    print("Se contaron los empleados: ",resultado)
    return jsonify({'result': resultado}), 200, {'Content-Type': 'application/json'}

@app.route('/ContVentas',methods=['POST'])
def ContVentas():
    query = "SELECT TOTALVENTAS FROM CONTADORVENTAS WHERE ID_CONTADOR = 1"
    resultado = obtenerDatos(query)
    print("Se mostro el contador de ventas: ",resultado)
    return jsonify({'result': resultado}), 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")
    app.run(debug=True)