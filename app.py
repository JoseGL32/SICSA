# -*- coding: utf-8 -*-
from base64 import b64decode
import webbrowser
from werkzeug.utils import secure_filename
import ipapi
from datetime import datetime,date, timedelta
from io import BytesIO
from PIL import Image
import random
import os
from werkzeug.exceptions import default_exceptions
from os import remove
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, sessions, url_for, session
from jinja2 import Environment
from werkzeug.security import check_password_hash, generate_password_hash

UPLOAD_FOLDER = os.path.abspath("./static/Imagenes/Reportes/")
UPLOAD_FOLDER1 = os.path.abspath("./static/Imagenes/Empleado/Firmas")
UPLOAD_FOLDER2 = os.path.abspath("./templates/rrhhimg")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER1"] = UPLOAD_FOLDER1
app.config["UPLOAD_FOLDER2"] = UPLOAD_FOLDER2

db1 = SQL("sqlite:///SCISA_DB.db")
app.secret_key = "super secret key"
app.jinja_env.add_extension('jinja2.ext.do')
jinja_env = Environment(extensions=['jinja2.ext.do'])


@app.route('/')
def Index():
    return render_template('login.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        # SELECT U.User, U.Contraseña, ur.idRole as Rol FROM Usuario as U inner join UserRole as ur on U.User=ur.idUser Where U.User=:username
        # Query database for username
        # HASHEAR USUARIOS 
        # db1.execute("Update Usuario set Contraseña = :userhash WHERE Usuario =:user",
        #               userhash=generate_password_hash("123"), user="Mario")      
        if usuario == "" or contraseña == "":
            return render_template('login.html', hola=1)
        else:
            rows = db1.execute("SELECT * FROM Usuario Where Usuario=:username",
                               username=usuario)
            
            if len(rows) == 0 or not check_password_hash(rows[0]["Contraseña"], contraseña):
                return render_template('login.html', hola=1)
            else:
                # Estas consultas son para mostrar la lista de personas y su asistencia
                hi = datetime.now()
                himes = hi.month
                # db.execute('INSERT INTO Registro VALUES (:usuario,:fecha,:salida,:horae,:horas,:trab,:mes)',
                #            usuario=usuario, fecha=datetime.date(hi), salida=NULL, horae=datetime.time(hi), horas=NULL, trab=NULL, mes=himes)
                ip = ipapi.location(output='json')
                print(ip)
                ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
                db1.execute('INSERT INTO RegistroTrabajadores VALUES (NULL,:usuario,:fecha,:salida,:horae,:horas,:trab,:ip)',
                            usuario=rows[0]["Id_Usuario"], fecha=datetime.date(hi), salida="", horae=datetime.time(hi), horas="", trab="", ip=ip_addr)
                
                empleado = db1.execute(
                    "select substr(emp.Nombre,1,5) as nom from Empleado as emp INNER JOIN Usuario as u on emp.Id_Empleado = u.IdEmpleado WHERE u.Usuario =:u", u=usuario)
                empleado1 = db1.execute(
                    "select emp.* from Empleado as emp INNER JOIN Usuario as u on emp.Id_Empleado = u.IdEmpleado WHERE u.Usuario =:u", u=usuario)

                # # Recordar el usuario y rol que se logeo
                session["user"] = empleado[0]["nom"]
                session["usercom"] = empleado1[0]["Nombre"]
                session["emp_id"] = empleado1[0]["Id_Empleado"]
                session["user_Id"] = rows[0]["Id_Usuario"]
                session["userrole"] = rows[0]["Id_Rol"]
                validacion = db1.execute(
                    "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_empleado = u.IdEmpleado WHERE u.Id_Usuario = :u", u=session["user_Id"])
                if validacion[0]["Estado"] == 'Pendiente':
                    return render_template("firma.html")
                return redirect(url_for('home'))
    else:
        return "render_template()"


@app.route('/asistencia', methods=["GET", "POST"])
def asistencia():
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hi = datetime.now()
    himes = hi.month
    prueba1 = db1.execute(
        "SELECT emp.Id_Empleado,emp.Nombre,rt.FechaEntrada,rt.FechaSalida,rt.HoraEntrada,rt.HoraSalida,rt.HorasTrabajadas,rt.Ip FROM RegistroTrabajadores as rt INNER JOIN Usuario as u ON rt.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE strftime('%m', rt.FechaEntrada) = :t", t="0"+str(himes))
    
    # print(prueba1[0]['Ip'])
    asistencia = db1.execute(
        'SELECT rt.IdUsuario,emp.Nombre,rt.FechaEntrada,rt.FechaSalida,rt.HoraEntrada,rt.HoraSalida,rt.HorasTrabajadas FROM RegistroTrabajadores as rt INNER JOIN Usuario as u ON rt.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado GROUP BY emp.Nombre')
    
    return render_template('Asistencia.html', mes=meses[himes], listas=prueba1, asist=asistencia, usuario=prueba1)


@app.route('/mostratrasistencia', methods=["GET", "POST"])
def mostrarasistencia():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.month
        sele = request.form['seleccion']
        user = request.form['seleccion1']
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        if user == "todo":
            prueba1 = db1.execute(
            "SELECT emp.Id_Empleado,emp.Nombre,rt.FechaEntrada,rt.FechaSalida,rt.HoraEntrada,rt.HoraSalida,rt.HorasTrabajadas,rt.Ip FROM RegistroTrabajadores as rt INNER JOIN Usuario as u ON rt.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE strftime('%m', rt.FechaEntrada) = :t", t="0"+str(himes))
        else:
            prueba1 = db1.execute(
            "SELECT emp.Id_Empleado,emp.Nombre,rt.FechaEntrada,rt.FechaSalida,rt.HoraEntrada,rt.HoraSalida,rt.HorasTrabajadas FROM RegistroTrabajadores as rt INNER JOIN Usuario as u ON rt.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE strftime('%m', rt.FechaEntrada) = :t AND rt.IdUsuario = :us", t=sele, us=user)
        asistencia = db1.execute(
            'SELECT rt.IdUsuario,emp.Nombre,rt.FechaEntrada,rt.FechaSalida,rt.HoraEntrada,rt.HoraSalida,rt.HorasTrabajadas FROM RegistroTrabajadores as rt INNER JOIN Usuario as u ON rt.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado GROUP BY emp.Nombre')
        
        return render_template('Asistencia.html', mes=meses[int(sele)], listas=prueba1, asist=asistencia)

    else:

        return redirect(url_for("index"))

@app.route('/mapa/<string:ip>')
def mapa(ip):
    data = ipapi.location(ip=ip, output='json')
    print(data)
    print(data['latitude'])
    return redirect("https://www.google.com/maps/search/?api=1&query="+str(data['latitude'])+","+str(data['longitude']))
    # return redirect(url_for("asistencia"))


@app.route('/deslog')
def deslog():
    hi = datetime.now()
    himes = hi.month
    ip = ipapi.location(output='json')
    print(ip)
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    # request.remote_addr ip local
    # primero ejecutamos un select para capturar el id del registro
    id = db1.execute('SELECT * FROM RegistroTrabajadores WHERE FechaEntrada = :fe AND FechaSalida = :salida AND Ip = :ip',
                fe=datetime.date(hi), salida="", ip=ip_addr)
    db1.execute('UPDATE  RegistroTrabajadores SET FechaSalida = :sal, HoraSalida = :horasal WHERE Id_Registro = :id',
                sal=datetime.date(hi), horasal=datetime.time(hi),  id = id[0]['Id_Registro'])
    
    hora_trabajadas = db1.execute('SELECT strftime("%H", HoraSalida) - strftime("%H", HoraEntrada) AS HorasTrab from RegistroTrabajadores WHERE Id_Registro = :id',
                                   id = id[0]['Id_Registro'])
    
    
    print(hora_trabajadas)
    db1.execute('UPDATE  RegistroTrabajadores SET HorasTrabajadas = :ht WHERE Id_Registro = :id',
                 ht = hora_trabajadas[0]['HorasTrab'],id=id[0]['Id_Registro'])
    session.clear()
    return render_template('login.html')


@app.route('/Cotizacion', methods = ["GET","POST"])
def cotizacion():
     datastatement = 1
     output = request.get_json('application/json',datastatement)
     cot = db1.execute(" select * from (select * from Cotizacion order by Id_Cotizacion ASC ) order by Id_Cotizacion DESC ")
     completado = db1.execute("SELECT COUNT(IdEstado)From Cotizacion WHERE IdEstado = :estado",estado = 4)
     Incompleto = db1.execute("SELECT COUNT(IdEstado)From Cotizacion WHERE IdEstado = :estado",estado = 5)
     Progreso = db1.execute("SELECT COUNT(IdEstado)From Cotizacion WHERE IdEstado = :estado",estado = 6)     
     Nselec = db1.execute('select Compañia,Id_Cliente from Cliente')
     if request.method == "POST":    
        typo1= 1
        typo2 =2
        typo3 = 4
        typo4 = 5
        if output:
           print("if output:")
           salida = json.loads(output)
           print(salida)
           if output!="":
              print("if output!="":")
              if salida['typo']== typo1:
                  idmp= db1.execute("select Id_MaterialProyecto from MaterialProyecto where Nombre = :salidas",salidas=salida["selected"])
                  print(idmp[0]['Id_MaterialProyecto'])
                  print('------')
                  cantidad = salida["numero"]
                  cost = salida["costo"]
                  print(cantidad)
                  id=1
                  db1.execute('Insert INTO DT_MProyect VALUES(null,:Cantida,:Id_Cot,:Id_MP,:value,:costo)', Cantida=cantidad,Id_Cot=id,Id_MP=idmp[0]['Id_MaterialProyecto'],value=0,costo = cost)
              elif salida['typo']== typo2: 
                  Mo= db1.execute("select Id_ManoObra from ManoObra where NombreMO = :salidas",salidas=salida["selected"])
                  cost = salida['costo']
                  db1.execute('Insert INTO Recursos VALUES(null,null,:IdManoObra,null,:CantidadMo,:value,:CostoMo)',IdManoObra=Mo[0]['Id_ManoObra'],CantidadMo = salida['numero'],value=0,CostoMo = cost)
              elif salida['typo']== typo4:
                   print('45544')
                   db1.execute('Insert INTO decripcionCot VALUES(null,:Idcot,:Descripccion)', Idcot = 1,Descripccion= salida['descripcion'])
              elif salida['data_send']== typo3:
                  value = db1.execute('SELECT * FROM Cotizacion WHERE Id_Cotizacion = :idbus', idbus= salida["data"])
                  input =  ast.literal_eval(sys.argv[1])
                  salida = input
                  salida["sal"] = value
                  sys.stdout.flush()
             
        Nocot= request.form["NoCot"]
        Ver = request.form["Version"]
        cl = request.form.get('Nombre-cliente')
        dh= request.form["DH"]
        ds= request.form["Desc"]
        fp= datetime.now()
        fpss = datetime.strftime(fp,'%d-%m-%Y')
        fi=request.form["Fechainicio"]
        fis = datetime.strptime(fi, '%Y-%m-%d')
        fiss = datetime.strftime(fis,'%d-%m-%Y')
        fin= request.form["FechaFin"]
        fins = datetime.strptime(fin, '%Y-%m-%d')
        finss = datetime.strftime(fins,'%d-%m-%Y')
        ie= 6
        comprobante = db1.execute('select NoCotizacion from  Cotizacion where NoCotizacion =:noc ',noc =Nocot)
        print(comprobante)
        if len(comprobante) == 0:
         db1.execute('INSERT INTO Cotizacion VALUES (NULL,:FechaPropuesta,:FechaInicio,:FechaFin,:DiasValidos,:Descripcion,:NoCotizacion,:IdEstado,Null,:Version,:IdCliente)',
                     FechaPropuesta=fpss, FechaInicio=fiss, FechaFin=finss,DiasValidos = dh,Descripcion=ds,NoCotizacion=Nocot,IdEstado=ie, Version = Ver,IdCliente=cl)
        var = db1.execute('SELECT MAX(Id_Cotizacion) FROM Cotizacion')
        db1.execute('UPDATE DT_MProyect set Id_Cot =:var1 WHERE Id_Cot = 1',var1=var[0]['MAX(Id_Cotizacion)'])  
        db1.execute('UPDATE Recursos set IdCotizacion =:var1 WHERE value = 0',var1=var[0]['MAX(Id_Cotizacion)'])  
        db1.execute('UPDATE Recursos set value =:var1 WHERE value = 0',var1 = 1) 
        db1.execute('UPDATE decripcionCot set Idcot =:var1 WHERE Idcot = 1',var1=var[0]['MAX(Id_Cotizacion)'])   
                 
     recur = db1.execute("SELECT * FROM MaterialProyecto")
     fact = db1.execute("SELECT * FROM ManoObra")
     
     
     selectooption1 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =1)
     selectooption2 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =2)
     selectooption3 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =3)
     selectooption4 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =4)
     selectooption5 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =5)
     selectooption6 = db1.execute('select Nombre FROM MaterialProyecto where CodigoMarca =:option',option =6)
     selectp = db1.execute('select Parte from MaterialProyecto where Parte != ""')
     selectall = db1.execute('select * from MaterialProyecto')
     return render_template('cotizacion.html',selectalls = selectall,parte  = selectp  ,selectooptions6 = selectooption6,selectooptions5 = selectooption5, Ns= Nselec,selectooptions =selectooption1,selectooptions2 =selectooption2,selectooptions3 =selectooption3,selectooptions4 =selectooption4,pro = recur , pro1=fact,cots = cot,comp=completado[0]["COUNT(IdEstado)"],inco = Incompleto[0]["COUNT(IdEstado)"],prog = Progreso[0]["COUNT(IdEstado)"])



   


@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sele = request.form['selec-mes']

        if sele:

            if sele == 'todo':

                print("todo")
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                # solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                solicitudes = db1.execute("select p.*, est.NombreEstado from prestaciones as p INNER JOIN Empleado as e ON p.Id_Empleado = e.Id_Empleado INNER JOIN estado as est ON p.estado = est.Id_Estado WHERE est.Id_Estado = 6")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])

                return render_template('home.html', fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="",
                    indice="todo")

            else:
                print("mesesssssssssss")
                print(sele)
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                # solicitudes = db1.execute("SELECT * FROM Solicitudes")
                solicitudes = db1.execute("select p.*, est.NombreEstado from prestaciones as p INNER JOIN Empleado as e ON p.Id_Empleado = e.Id_Empleado INNER JOIN estado as est ON p.estado = est.Id_Estado WHERE est.Id_Estado = 6")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
                empleados = db1.execute(
                    "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_Empleado = u.IdEmpleado")

            return render_template('home.html', emp=empleados, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=str(0), proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                   img="", pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
            empleados = db1.execute(
                "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_Empleado = u.IdEmpleado")

            return render_template('home.html', emp=empleados, soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("cargaaaaaaaaaaaaaaaaaa")

        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session['user_Id'])
        # solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        solicitudes = db1.execute("select p.*, est.NombreEstado from prestaciones as p INNER JOIN Empleado as e ON p.Id_Empleado = e.Id_Empleado INNER JOIN estado as est ON p.estado = est.Id_Estado WHERE est.Id_Estado = 6")
                # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")
        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        tareas = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
        reportesemp = db1.execute(
            "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
        solicitudemp = db1.execute(
            "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
        empleados = db1.execute(
            "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_Empleado = u.IdEmpleado")
        clientes = db1.execute("SELECT * FROM Cliente")
        acta = db1.execute("SELECT a.*,p.Logo,emp.Nombre,emp.Apellido,est.NombreEstado,p.NombreProyecto FROM Acta as a INNER JOIN Proyecto as p ON a.IdProyecto = p.Id_Proyecto INNER JOIN Estado as est ON a.IdEstado = est.Id_Estado INNER JOIN Usuario as u ON a.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado")
        return render_template('home.html',acta = acta, cli=clientes, emp=empleados, soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="")


@app.route('/repespecifico', methods=["GET", "POST"])
def repespecifico():
    if request.method == "POST":
        sele1 = request.form['selec-año']
        sele = request.form['selec-emp']
        sele2 = request.form['selec-pro']
        if sele1:
            reportes_especificos = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE strftime('%Y', r.FechaOrden) = :año AND u.Id_Usuario = :nombre AND r.IdProyecto = :idp", año=sele1, nombre=sele, idp=sele2)
            if reportes_especificos:
                found= "1"
            else:
                found = ""
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
            empleados = db1.execute(
                "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_Empleado = u.IdEmpleado")
            return render_template('home.html',encontrar_rep = found, emp=empleados, soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reportes_especificos, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")

        else:
            print("biennnnnnnnnnnnn")
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])

            return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")

        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        tareas = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
        reportesemp = db1.execute(
            "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
        solicitudemp = db1.execute(
            "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])

        return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="")
#Buscar acta
@app.route('/actaespecifica', methods=["GET", "POST"])
def actaespecifica():
    if request.method == "POST":
        sele1 = request.form['selec-año']
        # sele = request.form['selec-emp']
        sele2 = request.form['codigo']
        print(sele1)
        print(sele2)
        if sele1:
            reportes_especificos = db1.execute(
                "SELECT a.*,p.Logo,emp.Nombre,NoCotizacion as CodigoCot,emp.Apellido,est.NombreEstado,p.NombreProyecto,emp.Firma,cli.Nombre as NombreCliente,cli.Apellido as ApellidoCliente,cli.Compañia,cli.CodigoProv FROM Acta as a INNER JOIN Proyecto as p ON a.IdProyecto = p.Id_Proyecto INNER JOIN Cliente as cli ON cotiz.IdCliente = cli.Id_Cliente INNER JOIN Cotizacion as cotiz ON p.Id_Proyecto = cotiz.IdProyecto INNER JOIN Estado as est ON a.IdEstado = est.Id_Estado INNER JOIN Usuario as u ON a.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE strftime('%Y', a.FechaFin) = :año  AND cli.CodigoProv = :idp", año=sele1, idp=sele2)
            if reportes_especificos:
                found= "1"
            else:
                found = ""
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
            empleados = db1.execute(
                "SELECT * FROM Empleado as emp INNER JOIN Usuario as u ON emp.Id_Empleado = u.IdEmpleado")
            return render_template('home.html',encontrar = found, emp=empleados, soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, acta=reportes_especificos, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")

        else:
            print("biennnnnnnnnnnnn")
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])

            return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")

        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        tareas = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
        reportesemp = db1.execute(
            "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
        solicitudemp = db1.execute(
            "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])

        return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="")


# mostrar los modals segun su seleccion
@app.route('/modal')
def modal():
    # proyectos = db.execute("SELECT * FROM Proyectos")
    # permisos = db.execute("SELECT * FROM Solicitudes")
    return render_template('modal.html', pro=proyectos, permiso=permisos)

@app.route('/busquedapro', methods=["GET", "POST"])
def busquedapro():
    if request.method == "POST":
        proyecto = request.form['busqueda']
        busqueda = db1.execute('SELECT strftime("%m",FechaHoraInicio) as mes FROM Proyecto WHERE NombreProyecto = :busq',busq = proyecto)
        
        return redirect(url_for( 'home2' ,info=busqueda[0]['mes']))
    

@app.route('/reporte', methods=["GET", "POST"])
def reporte():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.date()
        tarea = request.form['tarea']
        cliente = request.form['cliente']
        contacto = request.form['contacto']
        correo = request.form['correo']
        horae = request.form['horaent']
        horasal = request.form['horasal']
        porcentaje = request.form['porcentaje']
        proyecto = request.form['selec-pro']
        descripcion = request.form['descripcion']
        # Esto es para leer la firma de un html
        # firma = request.form['signature']
        imagen = request.files['imagen']  # SE CAMBIO IMAGEN POR SIGNATURE
        nombreimagen = imagen.filename
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreimagen))
        ruta = "../static/Imagenes/Reportes/" + nombreimagen
        # # DIRMA ES UN BASE64 STRING HAY QUE DECODIFICARLO
        # im = Image.open(BytesIO(b64decode(firma.split(',')[1])))
        # im.save(os.path.join(
        #     app.config["UPLOAD_FOLDER1"], "firma"+str(session[
        #         "user_Id"])+".png"))
        # rutafirma = "../static/Imagenes/Empleado/Firmas/" + "firma"+str(session[
        #     "user_Id"])+".png"
        # db.execute("INSERT INTO Reportes VALUES(NULL,:nom,:porcen,:desc,:img)",
        #            nom=tarea, porcen=porcentaje, desc=descripcion, img=imagen)
        db1.execute("INSERT INTO Reporte VALUES(NULL,:porcen,:Contacto,:Cliente,:user,:correo,:horaent,:horasal,:nom,:desc,:img,:fecha,:rep)",
                    porcen=porcentaje, Contacto=contacto, Cliente=cliente, user=session[
                        "user_Id"], correo=correo, horaent=horae, horasal=horasal, nom=tarea, desc=descripcion, img=ruta, fecha=himes, rep=proyecto)
        flash('Reporte Creado')
        return redirect(url_for('success'))
    else:
        return redirect(url_for("index"))


@app.route('/firma', methods=["GET", "POST"])
def firma():
    if request.method == "POST":
        # Esto es para leer la firma de un html
        firma = request.form['signature']
        # # DIRMA ES UN BASE64 STRING HAY QUE DECODIFICARLO
        im = Image.open(BytesIO(b64decode(firma.split(',')[1])))
        im.save(os.path.join(
            app.config["UPLOAD_FOLDER1"], "firma"+str(session[
                "user_Id"])+".png"))
        rutafirma = "../static/Imagenes/Empleado/Firmas/" + "firma"+str(session[
            "user_Id"])+".png"
        db1.execute("UPDATE Empleado SET Estado = :act, Firma = :fir WHERE Id_Empleado = :id",
                    act="Activo", fir=rutafirma,id = session["emp_id"])
        return jsonify({'status': 200})
    else:
        return redirect(url_for("index"))


@app.route('/reporteemp', methods=["GET", "POST"])
def reporteemp():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.date()
        tarea = request.form['tarea']
        cliente = request.form['cliente']
        contacto = request.form['contacto']
        correo = request.form['correo']
        horae = request.form['horaent']
        horasal = request.form['horasal']
        porcentaje = request.form['porcentaje']
        proyecto = request.form['selec-pro']
        descripcion = request.form['descripcion']
        # Esto es para leer la firma de un html
        # firma = request.form['firma']
        imagen = request.files['imagen']  # SE CAMBIO IMAGEN POR SIGNATURE
        nombreimagen = imagen.filename
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreimagen))
        ruta = "../static/Imagenes/Reportes/" + nombreimagen
        # DIRMA ES UN BASE64 STRING HAY QUE DECODIFICARLO
        # im = Image.open(BytesIO(b64decode(firma.split(',')[1])))
        # im.save(os.path.join(
        #     app.config["UPLOAD_FOLDER1"], "firma"+str(session[
        #         "user_Id"])+".png"))
        # rutafirma = "../static/Imagenes/Empleado/Firmas/" + "firma"+str(session[
        #     "user_Id"])+".png"
    # db.execute("INSERT INTO Reportes VALUES(NULL,:nom,:porcen,:desc,:img)",
    #            nom=tarea, porcen=porcentaje, desc=descripcion, img=imagen)
        db1.execute("INSERT INTO Reporte VALUES(NULL,:porcen,:Contacto,:Cliente,:user,:correo,:horaent,:horasal,:nom,:desc,:img,:fecha,:rep)",
                    porcen=porcentaje, Contacto=contacto, Cliente=cliente, user=session[
                        "user_Id"], correo=correo, horaent=horae, horasal=horasal, nom=tarea, desc=descripcion, img=ruta, fecha=himes, rep=proyecto)
        return redirect(url_for('success'))
    else:
        return redirect(url_for("index"))

@app.route('/success')
def success():
    return render_template('success.html')
@ app.route('/reporteprint/<string:rep>', methods=["GET", "POST"])
def reporteprint(rep):
    reporteesp = db1.execute(
        "select r.*, em.Nombre,em.Firma from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=rep)
    print("rep conbsulta: ", reporteesp)

    if request.method == "POST":
        print(reporteesp)
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])

                return render_template('home.html', fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="",
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
                reporteesp = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=1)

                return render_template('home.html', fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img="", pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reporteesp = db1.execute(
                "select r.*,p.*, em.Nombre, from Reporte as r INNER JOIN Proyecto as p ON r.IdProyecto = p.Id_Proyecto INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=rep)
            print(reporteesp)
            hi = datetime.now()
            reportesemp = db1.execute(
                "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
            return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha=datetime.date(hi),  repesp=reporteesp, tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")
        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT * FROM Solicitudes")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        tareas = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
        reporteesp = db1.execute(
            "select r.*, em.Nombre,em.Firma,p.NombreProyecto from Reporte as r INNER JOIN Proyecto as p ON r.IdProyecto = p.Id_Proyecto INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=rep)
        print(reporteesp)
        hi = datetime.now()
        reportesemp = db1.execute(
            "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
        solicitudemp = db1.execute(
            "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
        return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha=datetime.date(hi),  repesp=reporteesp, tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                               incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                               soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
            0]["COUNT(IdEstado)"],
            prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")

@ app.route('/actaprint/<string:acta>', methods=["GET", "POST"])
def actaprint(acta):
    print(acta)
    #hacemos la consulta que nos trae la informacion del acta y todo lo que se va a mostrar en el pdf
    actesp = db1.execute(
        "SELECT a.*,p.Logo,emp.Nombre,NoCotizacion as CodigoCot,emp.Apellido,est.NombreEstado,p.NombreProyecto,emp.Firma,cli.Nombre as NombreCliente,cli.Apellido as ApellidoCliente,cli.Compañia,cli.CodigoProv FROM Acta as a INNER JOIN Proyecto as p ON a.IdProyecto = p.Id_Proyecto INNER JOIN Cliente as cli ON cotiz.IdCliente = cli.Id_Cliente INNER JOIN Cotizacion as cotiz ON p.Id_Proyecto = cotiz.IdProyecto INNER JOIN Estado as est ON a.IdEstado = est.Id_Estado INNER JOIN Usuario as u ON a.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE a.Id_Acta = :i", i=acta)
    print("act conbsulta: ", actesp)
    tareas = db1.execute(
        "select at.Titulo from AsignacionTarea as at LEFT JOIN Planeacion as pl ON at.IdPlaneacion = pl.Id_Planeacion LEFT JOIN Proyecto as pr ON pl.IdProyecto= pr.Id_Proyecto WHERE pr.Id_Proyecto = :idpro", idpro=actesp[0]['IdProyecto'])
    print("tareas conbsulta: ", tareas)
    if request.method == "POST":
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])

                return render_template('home.html', fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="",
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
                reporteesp = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=1)

                return render_template('home.html', fecha="", repesp="", tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img="", pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            tareas = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
            reporteesp = db1.execute(
                "select r.*,p.*, em.Nombre, from Reporte as r INNER JOIN Proyecto as p ON r.IdProyecto = p.Id_Proyecto INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado WHERE r.Id_Reporte = :i", i=rep)
            print(reporteesp)
            hi = datetime.now()
            actesp = db1.execute(
            "SELECT a.*,p.Logo,emp.Nombre,emp.Apellido,emp.Firma,est.NombreEstado,p.NombreProyecto FROM Acta as a INNER JOIN Proyecto as p ON a.IdProyecto = p.Id_Proyecto INNER JOIN Estado as est ON a.IdEstado = est.Id_Estado INNER JOIN Usuario as u ON a.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE a.Id_Acta = :i", i=acta)
            solicitudemp = db1.execute(
                "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
            return render_template('home.html', soliemp=solicitudemp, repemp=reportesemp, fecha=datetime.date(hi),  actesp=actesp, tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")
        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select * from Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT * FROM Solicitudes")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        tareas = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])
        actesp = db1.execute(
        "SELECT a.*,p.Logo,emp.Nombre,NoCotizacion as CodigoCot,emp.Apellido,est.NombreEstado,p.NombreProyecto,emp.Firma,cli.Nombre as NombreCliente,cli.Apellido as ApellidoCliente,cli.Compañia,cli.CodigoProv FROM Acta as a INNER JOIN Proyecto as p ON a.IdProyecto = p.Id_Proyecto INNER JOIN Cliente as cli ON cotiz.IdCliente = cli.Id_Cliente INNER JOIN Cotizacion as cotiz ON p.Id_Proyecto = cotiz.IdProyecto INNER JOIN Estado as est ON a.IdEstado = est.Id_Estado INNER JOIN Usuario as u ON a.IdUsuario = u.Id_Usuario INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE a.Id_Acta = :i", i=acta)
        
        hi = datetime.now()
        reportesemp = db1.execute(
            "SELECT * FROM Reporte WHERE IdUsuario = :u", u=session["user_Id"])
        solicitudemp = db1.execute(
            "SELECT * FROM Solicitudes WHERE IdUsuario = :u", u=session["user_Id"])
        tareasacta = db1.execute(
        "select at.Titulo from AsignacionTarea as at LEFT JOIN Planeacion as pl ON at.IdPlaneacion = pl.Id_Planeacion LEFT JOIN Proyecto as pr ON pl.IdProyecto= pr.Id_Proyecto WHERE pr.Id_Proyecto = :idpro", idpro=actesp[0]['IdProyecto'])
        return render_template('home.html',taracta = tareasacta, soliemp=solicitudemp, repemp=reportesemp, fecha=datetime.date(hi),  actesp=actesp, tar=tareas, rep=reporte, var1="", completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                               incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                               soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
            0]["COUNT(IdEstado)"],
            prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")


@ app.route('/solicitud', methods=["GET", "POST"])
def solicitud():
    if request.method == "POST":
        hi = datetime.now()
        titulo = request.form['titulo']
        justificacion = request.form['justificacion']
        db1.execute('INSERT INTO Solicitudes VALUES(null, :nom, :jus, :fech, :titu, :estado, :vi)',
                    nom=session["user_Id"], jus=justificacion, fech=datetime.date(hi), titu=titulo, estado=6, vi=1)
        return redirect(url_for('home'))
    else:

        return redirect(url_for("index"))


@ app.route('/AceptarSoli', methods=["GET", "POST"])
def AceptarSoli():
    if request.method == "POST":
        id = request.form['resp']

        db1.execute('UPDATE Solicitudes SET IdEstado = :est,Vigencia = :vi WHERE Id_Solicitud = :Id',
                    est=4, vi=1, Id=id)
        return redirect(url_for('home'))

    else:

        return redirect(url_for("index"))


@ app.route('/Vernot', methods=["GET", "POST"])
def Vernot():
    if request.method == "POST":
        vigencia = request.form['resp']
        db1.execute("UPDATE Solicitudes SET Vigencia = :vi where Vigencia = 1",
                    vi=int(vigencia))

        return redirect(url_for('home'))

    else:

        return redirect(url_for("index"))


@ app.route('/home1/<string:info>')
def home1(info):
    if request.method == "POST":
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])

                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")

                return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="",
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                print(indice)
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")

                return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img="", pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            variable = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")
           
        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        variable = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        
        return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="")


#HOME DEL BUSCAR
@ app.route('/home2/<string:info>')
def home2(info):
    if request.method == "POST":
        sele = request.form['selec-mes']
        if sele:
            if sele == 'todo':
                print("todo")
                proyectos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
                proyectos_user = db1.execute(
                    "select * from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado= :estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                tareas = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE e.Nombre = :user1", user1=session["usercom"])

                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")

                return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                       incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes,
                                       comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0][
                    "COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="",
                    indice="todo")

            else:
                print("meses")
                proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=sele)
                proyectos_user = db1.execute(
                    "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
                solicitudes = db1.execute("SELECT * FROM Solicitudes")
                # contar los proyectos aprobados, incompletos y en progreso
                completado = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
                Incompleto = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
                Progreso = db1.execute(
                    "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

                total = db1.execute("SELECT COUNT(*) FROM Proyecto")
                cuentaComp = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
                cuentaPro = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
                cuentaInc = db1.execute(
                    "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
                indice = "mes"
                print(indice)
                variable = db1.execute(
                    "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
                reporte = db1.execute(
                    "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")

                return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=0, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"],
                                       img="", pro_espe=proyectos_especificos, indice="mes")
        else:
            print("afuera del if de todo")
            proyectos = db1.execute(
                "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
            proyectos_user = db1.execute(
                "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
            solicitudes = db1.execute("SELECT * FROM Solicitudes")
            # contar los proyectos aprobados, incompletos y en progreso
            completado = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
            Incompleto = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
            Progreso = db1.execute(
                "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

            total = db1.execute("SELECT COUNT(*) FROM Proyecto")
            cuentaComp = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
            cuentaPro = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
            cuentaInc = db1.execute(
                "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
            variable = db1.execute(
                "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
            reporte = db1.execute(
                "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
            return render_template('home.html', fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'],
                                   incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user,
                                   soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[
                0]["COUNT(IdEstado)"],
                prog=Progreso[0]["COUNT(IdEstado)"], img="", indice="todo")
    else:
        print("carga")
        print(info)
        if info:
            proyectos_especificos = db1.execute(
                    "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado WHERE strftime('%m', p.FechaHoraInicio) = :mes", mes=info)
            print(proyectos_especificos)
            indice1 = "mes"
        else:
            proyectos_especificos = ""
            indice1 = ""        
        proyectos = db1.execute(
            "SELECT * FROM Proyecto as p INNER JOIN Estado as e ON p.IdEstado = e.Id_Estado INNER JOIN Planeacion as pl ON pl.IdProyecto = p.Id_Proyecto INNER JOIN Empleado as em ON pl.IdEmpleado = em.Id_Empleado ORDER By p.Id_Proyecto")
        proyectos_user = db1.execute(
            "select p.NombreProyecto, e.Nombre from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado WHERE U.Id_Usuario=:user", user=session["user_Id"])
        solicitudes = db1.execute("SELECT soli.Id_Solicitud,e.Nombre, soli.Justificacion, soli.FechaSoli, soli.Titulo, est.NombreEstado, soli.Vigencia from Solicitudes as soli INNER JOIN Usuario as u On soli.IdUsuario = u.Id_Usuario INNER JOIN Empleado as e ON u.IdEmpleado = e.Id_Empleado INNER JOIN Estado as est ON soli.IdEstado = est.Id_Estado")
        # contar los proyectos aprobados, incompletos y en progreso
        completado = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Completado")
        Incompleto = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :estado", estado="Incompleto")
        Progreso = db1.execute(
            "SELECT COUNT(IdEstado)From Proyecto as p INNER JOIN Estado as e On p.IdEstado=e.Id_Estado WHERE e.NombreEstado=:estado", estado="Progreso")

        total = db1.execute("SELECT COUNT(*) FROM Proyecto")
        cuentaComp = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Completado", to=total[0]['COUNT(*)'])
        cuentaPro = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Progreso", to=total[0]['COUNT(*)'])
        cuentaInc = db1.execute(
            "SELECT count(*)*100 / :to AS calc From Proyecto as p INNER JOIN Estado as e On p.IdEstado = e.Id_Estado WHERE e.NombreEstado = :est", est="Incompleto", to=total[0]['COUNT(*)'])
        variable = db1.execute(
            "select p.NombreProyecto, e.Nombre,at.Titulo,at.FechaInicioEstimado,at.FechaFinEstimado,at.Descripcion,est.NombreEstado  from Proyecto as p INNER join Planeacion as pla ON pla.IdProyecto=p.Id_Proyecto INNER JOIN Empleado as e On pla.IdEmpleado=e.Id_Empleado INNER Join Usuario as u On e.Id_Empleado=u.IdEmpleado INNER JOIN AsignacionTarea as at ON pla.Id_Planeacion = at.IdPlaneacion INNER JOIN Estado as est ON at.IdEstado = est.Id_Estado WHERE p.Id_Proyecto= :user", user=info)
        reporte = db1.execute(
            "select r.*, em.Nombre from Reporte as r INNER JOIN Usuario as u ON r.IdUsuario= u.Id_Usuario INNER JOIN Empleado as em ON u.IdEmpleado = em.Id_Empleado")
        print(proyectos_especificos)
        return render_template('home.html',indice = indice1,pro_espe=proyectos_especificos, fecha="", tar="", rep=reporte, var1=variable, completo=cuentaComp[0]['calc'], progreso=cuentaPro[0]['calc'], incompleto=cuentaInc[0]['calc'], pro=proyectos, proUser=proyectos_user, soli=solicitudes, comp=completado[0]["COUNT(IdEstado)"], inco=Incompleto[0]["COUNT(IdEstado)"], prog=Progreso[0]["COUNT(IdEstado)"], img="")



@app.route('/facturacion', methods=["GET","POST"])
def facturacion():
      if request.method == "POST":
       adl= request.form["Adl"]
       fp= request.form["Fechaemision"]
       fps = datetime.strptime(fp, '%Y-%m-%d')
       fpss = datetime.strftime(fps,'%d-%m-%Y')
       fi=request.form["Fechacancelacion"]
       fis = datetime.strptime(fi, '%Y-%m-%d')
       fiss = datetime.strftime(fis,'%d-%m-%Y')
       idc= request.form["Idc"]
       idst = db1.execute('select IdEstado from Cotizacion where id_Cotizacion = :idE',idE=idc)
       idct= db1.execute('SELECT SUM(Cantidad * PrecioUnitario) as total from MaterialProyecto where IdCotizacion = :idc1',idc1 = idc)
       db1.execute('INSERT INTO Factura VALUES(NULL,:FechaEmision,:FechaCancelacion,:Adelanto,:IdCotizacion,:IdEstado,:Total)',
                       FechaEmision=fpss,FechaCancelacion=fiss,Adelanto=adl,IdCotizacion=idc,IdEstado= idst[0]["IdEstado"], Total=idct[0]["total"])
      return render_template('facturacion.html') 




@ app.route('/admin')
def admin():

    return render_template('administracion.html')


@ app.route('/aduser/<string:info>')
def aduser(info):
    empleados = db1.execute(
        "select emp.Id_Empleado,emp.Telefono,u.Usuario,u.Contraseña,u.Id_Rol,emp.Nombre,emp.Apellido,emp.Cedula,emp.Direccion,emp.Estado,emp.salario,emp.fechacontrato,emp.CamisaTalla,emp.ZapatoTalla,emp.Cargo from Usuario as u INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE emp.Id_Empleado = :i", i=info)

    return render_template('aduser.html', empinfo=empleados)


@ app.route('/eliminaruser/<string:info>')
def eliminaruser(info):
    empleados = db1.execute(
        "UPDATE Empleado SET Estado = :est WHERE Id_Empleado = :i", est="Inactivo", i=info)
    empleados = db1.execute(
        "select emp.Id_Empleado,u.Usuario,u.Contraseña,u.Id_Rol,emp.Nombre,emp.Apellido,emp.Cedula,emp.Direccion,emp.Estado from Usuario as u INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE emp.Estado =:act OR emp.Estado = 'Pendiente'", act="Activo")

    return render_template('veremp.html', empinfo=empleados,accion = "eliminar")


@ app.route('/añadiremp', methods=["GET", "POST"])
def añadiremp():
    if request.method == "POST":
        nombres = request.form['nombre']
        nombre = request.form['nombre1']
        apellidos = request.form['apellido']
        apellido = request.form['apellido1']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        rol = request.form['rol']
        salario = request.form['salario']

        fechaContrato = request.form['fechacontrato']
        tallaCamisa = request.form['camisa']
        tallazapatos = request.form['tallazapato']
        cargo = request.form['puesto']
        db1.execute("INSERT INTO Empleado VALUES(NULL,:name,:lastna,:ced,:dir,:tel,:est,NULL,NULL,:salario,:fechacontrato,:camisat,:zapta,:carg)",
                    name=nombres + nombre, lastna=apellidos + apellido, ced=cedula, dir=direccion,tel = telefono, est='Pendiente',salario = salario,
                    fechacontrato =fechaContrato,camisat = tallaCamisa,zapta = tallazapatos,carg = cargo )
        idempleado = db1.execute(
            "SELECT * FROM Empleado WHERE Cedula = :ced", ced=cedula)

        longitud = 8
        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

        p = ""
        p = p.join([random.choice(valores) for i in range(longitud)])
        db1.execute("INSERT INTO Usuario VALUES(NULL,:us,:contra,:rol,:idemp)",
                    us=str(nombres+"."+apellidos), contra=generate_password_hash(p), rol=int(rol), idemp=idempleado[0]['Id_Empleado'])
        datos = db1.execute(
            "SELECT * FROM Usuario WHERE IdEmpleado = :idemp", idemp=idempleado[0]['Id_Empleado'])
        print(datos)
        return render_template('verificacion.html', cred=datos, cont=p)
    print('afueraaaaaaaaa')
    return redirect(url_for('veremp'))


@ app.route('/añadircli', methods=["GET", "POST"])
def añadircli():
    if request.method == "POST":
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        cedula = request.form['cedula']
        compañia = request.form['compañia']
        telefono = request.form['telefono']
        email = request.form['correo']
        codigo = request.form['codigo']
        direccion = request.form['direccion']
        
        db1.execute("INSERT INTO Cliente VALUES(NULL,:name,:lastna,:ced,:comp,:tel,:dir,:email,:cod)",
                    name=nombres, lastna=apellidos, ced=cedula, comp=compañia, tel=telefono, dir=direccion, email=email,cod = codigo)

        return render_template('vercliente.html', registro="exito")
    print('afueraaaaaaaaa')
    return redirect(url_for('vercli'))


@ app.route('/adclientes/<string:info>')
def adclientes(info):
    cliente = db1.execute(
        "select * FROM Cliente WHERE Id_Cliente = :i", i=info)
    return render_template('adclientes.html', clinfo=cliente)


@ app.route('/usuarioesp', methods=["GET", "POST"])
def usuarioesp():
    if request.method == "POST":
        emplea = request.form['sele-adm-emp']
        empleados = db1.execute(
            "select emp.Id_Empleado,u.Usuario,u.Contraseña,u.Id_Rol,emp.Nombre,emp.Apellido,emp.Cedula,emp.Direccion,emp.Estado,emp.salario,emp.fechacontrato,emp.CamisaTalla,emp.ZapatoTalla,emp.Cargo from Usuario as u INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE emp.Id_Empleado = :id", id=emplea)

    return render_template('aduser.html', empinfo=empleados)


@ app.route('/clientesp', methods=["GET", "POST"])
def clientesp():
    if request.method == "POST":
        emplea = request.form['sele-adm-cli']
        clientes = db1.execute(
            "select * FROM Cliente as c WHERE c.Id_Cliente = :id", id=emplea)

    return render_template('adcliente.html', clinfo=clientes)


@ app.route('/actualizardatos', methods=["GET", "POST"])
def actualizardatos():
    if request.method == "POST":
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        rol = request.form['rol']
        salario = request.form['salario']

        fechaContrato = request.form['fechacontrato']
        tallaCamisa = request.form['camisa']
        tallazapatos = request.form['tallazapato']
        cargo = request.form['puesto']
        db1.execute(
            "Update Empleado set Nombre = :user,Apellido = :apellido,Cedula = :cedula,Direccion = :dir,Telefono = :tel,salario=:sal,fechacontrato=:fe,CamisaTalla = :ca,ZapatoTalla = :za,Cargo = :car WHERE Id_Empleado =:id", user=nombre, apellido=apellido, cedula=cedula, dir=direccion,tel = telefono,sal = salario,fe = fechaContrato,ca=tallaCamisa,za = tallazapatos,car=cargo, id=id)
        db1.execute("UPDATE Usuario SET Id_Rol = :rolnuevo WHERE IdEmpleado = :idemp",rolnuevo = rol,idemp = id)
    return redirect(url_for('veremp'))


@ app.route('/actualizardatoscli', methods=["GET", "POST"])
def actualizardatoscli():
    if request.method == "POST":
        id = request.form['Id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        compañia = request.form['compañia']
        telefono = request.form['telefono']
        correo = request.form['correo']
        codigo = request.form['codigo']
        db1.execute(
            "Update Cliente set Nombre = :user,Apellido = :apellido,Cedula = :cedula,Direccion = :dir,Compañia=:com,Telefono = :t,Email = :co,CodigoProv = :cod WHERE Id_Cliente =:id", user=nombre, apellido=apellido, cedula=cedula, dir=direccion, com=compañia, t=telefono, co=correo,cod = codigo, id=id)

    return redirect(url_for('vercliente'))


@ app.route('/admateriales')
def admateriales():
    if request.method == "POST":
        hi = datetime.now()
        himes = hi.date()
        tarea = request.form['tarea']

    return render_template('admateriales.html')


@ app.route('/veremp')
def veremp():
    empleados = db1.execute(
        "select emp.Id_Empleado,u.Usuario,u.Contraseña,u.Id_Rol,emp.Nombre,emp.Apellido,emp.Cedula,emp.Direccion,emp.Estado,emp.salario,emp.fechacontrato,emp.CamisaTalla,emp.ZapatoTalla,emp.Cargo from Usuario as u INNER JOIN Empleado as emp ON u.IdEmpleado = emp.Id_Empleado WHERE emp.Estado =:act OR emp.Estado = 'Pendiente'", act="Activo")

    return render_template('veremp.html', empinfo=empleados)


@ app.route('/vercliente')
def vercliente():
    empleados = db1.execute(
        "select * FROM Cliente")

    return render_template('vercliente.html', empinfo=empleados)



@ app.route('/planificacion')
def planificacion():

    return render_template('planificacion.html')

@ app.route('/ejecucion')
def ejecucion():
    proyectos = db1.execute(
        "SELECT p.*,est.NombreEstado FROM Proyecto as p INNER JOIN Estado as est ON p.IdEstado = est.Id_Estado")

    return render_template('ejecucion.html', pro=proyectos, tarea="", tarea1="")


@ app.route('/ejecucion1/Proyecto:<string:id>')
def ejecucion1(id):
    if request.method == "POST":
        proyectos = db1.execute(
            "SELECT p.*,est.NombreEstado FROM Proyecto as p INNER JOIN Estado as est ON p.IdEstado = est.Id_Estado")
        tareas = db1.execute("select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE pro.Id_Proyecto=:idp", idp=id)

        return render_template('ejecucion.html', pro=proyectos, tarea=tareas, tarea1="")
    else:
        proyectos = db1.execute(
            "SELECT p.*,est.NombreEstado FROM Proyecto as p INNER JOIN Estado as est ON p.IdEstado = est.Id_Estado")
        tareas = db1.execute("select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE pro.Id_Proyecto=:idp", idp=id)
        return render_template('ejecucion.html', pro=proyectos, tarea=tareas, tarea1="")


@ app.route('/ejecucion2/Tarea:<string:id>')
def ejecucion2(id):
    if request.method == "POST":
        proyectos = db1.execute(
            "SELECT p.*,est.NombreEstado FROM Proyecto as p INNER JOIN Estado as est ON p.IdEstado = est.Id_Estado")
        tareasdesc = db1.execute("select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE at.Id_Asignacion=:idt", idt=id)
        proyecid = db1.execute("select pro.Id_Proyecto from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE at.Id_Asignacion=:idt", idt=id)

        tareas = db1.execute("select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE pro.Id_Proyecto=:idp", idp=proyecid)
        return render_template('ejecucion.html', pro=proyectos, tarea=tareas, tarea1=tareasdesc)
    else:
        proyectos = db1.execute(
            "SELECT p.*,est.NombreEstado FROM Proyecto as p INNER JOIN Estado as est ON p.IdEstado = est.Id_Estado")
        tareasdesc = db1.execute("select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE at.Id_Asignacion=:idt", idt=id)
        proyecid = db1.execute("select pro.Id_Proyecto from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE at.Id_Asignacion=:idt", idt=id)

        tareas = db1.execute(
            "select at.*, est.NombreEstado, em.Nombre from AsignacionTarea as at INNER JOIN Empleado as em ON at.IdEmpleado=em.Id_Empleado INNER JOIN Estado as est ON at.IdEstado=est.Id_Estado INNER JOIN Planeacion as pl ON at.IdPlaneacion=pl.Id_Planeacion INNER JOIN Proyecto as pro ON pro.Id_Proyecto=pl.IdProyecto WHERE pro.Id_Proyecto=:idp", idp=proyecid[0]['Id_Proyecto'])
        return render_template('ejecucion.html', pro=proyectos, tarea=tareas, tarea1=tareasdesc)
#generar acta de entrega
@app.route('/acta', methods = ["GET","POST"])
def acta():
    if request.method == "POST":
        idproyecto = request.form['selec-pro']
        estado = request.form['selec-est']
        fechafin = request.form['fechafin']
        horafin = request.form['horafin']
        obs = request.form['observaciones']
        db1.execute("UPDATE Proyecto set IdEstado = :est, FechaHoraFin  = :f WHERE Id_Proyecto = :pro",est =estado,f = fechafin,pro = idproyecto )
        db1.execute("INSERT INTO Acta VALUES(NULL,:proyecto,:fechafin,:horafin,:observ,:est,:us)",proyecto = idproyecto,fechafin = fechafin,horafin = horafin,observ = obs,est = estado,us = session["user_Id"])
        return redirect(url_for('home'))
    return "1"

@ app.route('/perfil')
def perfil():

    return render_template('perfil.html')

@ app.route('/ayuda')
def ayuda():

    return render_template('ayuda.html')
#*****************************************
@app.route('/src',methods=["GET","POST"])
def src():
    if request.method == "POST":
      name = request.form["name"]
      Pu= request.form["Precio"]
      Marcar = request.form["Marca"]
      Cm = request.form["CodigoMarca"]
      pv = request.form["Proveedor"]
      ics= db1.execute("SELECT MAX(Id_Cotizacion) AS ic FROM Cotizacion")
      pvid = db1.execute("SELECT  Nombre From Proveedor WHERE Id_Proveedor = :estado",estado = pv)
      db1.execute('INSERT INTO MaterialProyecto VALUES(NULL,:Nombre,:PrecioUnitario,:Marca,:CodigoMarca,:IdProveedor,)',
                  Nombre = name, PrecioUnitario=Pu, Marca = Marcar,CodigoMarca=Cm,IdProveedor=pvid[0]['Nombre'])
      
    return render_template("RecursoCot.html")  

@app.route('/Proyecto',methods=["GET","POST"])
def Proyecto():
     datastatement = 1
     codigodetalle = request.get_json('application/json',datastatement)
     id = request.args.get('id-cot')
     fp= datetime.now()
     fpss = datetime.strftime(fp,'%d-%m-%Y') 
     print(id)
     data=db1.execute('SELECT IdManoObra as id,NombreMO,CantidadMO FROM Recursos,ManoObra where IdCotizacion =:idC and id == Id_ManoObra',idC = id)
     print(data)
     data1=db1.execute('SELECT * from Cotizacion where Id_Cotizacion = :idb',idb = id)
     print('/**/')
     print(data1[0]['IdCliente'])
     cliente = db1.execute('select * from Cliente where Id_Cliente = :Idc ' ,Idc = data1[0]['IdCliente'] )
     print(cliente)
     idmp=db1.execute('SELECT Id_MP from DT_MProyect where Id_Cot = :idb',idb = id)
     print(len(idmp))
     x=len(idmp)
     valuepro = db1.execute('SELECT Id_Cotizacion,Descripcion,FechaInicio,FechaFin,Id_MP as idd,Nombre,Cantidad,IdManoObra as idr,NombreMO from Cotizacion,DT_MProyect,MaterialProyecto,Recursos,ManoObra WHERE Id_Cotizacion = :ids and Id_Cot =:ids AND idd = Id_MaterialProyecto AND IdCotizacion=86 AND idr = Id_ManoObra',ids = id)
    
     print(valuepro)   
     if request.method == "POST":   
          if codigodetalle:
              salida = json.loads(codigodetalle)
              print(salida)
              db1.execute('INSERT INTO DtalleOrden VALUES(null,:Codigoorden,:IdCliente,:Id_CotizacionD)',Codigoorden = salida['codigo'],IdCliente=data1[0]['IdCliente'],Id_CotizacionD = id)
              db1.execute('INSERT INTO Proyecto VALUES(null,:NombreProyecto,:FechaHoraInicio,:FechaHoraFin,:Ubicacion,:IdEstado)',NombreProyecto =  data1[0]['Descripcion'],FechaHoraInicio =data1[0]['FechaInicio'], FechaHoraFin = data1[0]['FechaFin'] , Ubicacion = salida['Ubicacion'] , IdEstado = 2 )
              db1.execute('UPDATE Cotizacion set IdEstado =:var1 WHERE Id_Cotizacion = :ids',var1 = 2 , ids = id)  
              MaxIdProy = db1.execute('SELECT MAX(Id_Proyecto) FROM Proyecto')
              print(MaxIdProy)
              db1.execute('UPDATE Cotizacion set IdProyecto =:var1 where Id_Cotizacion =:ids', var1 = MaxIdProy[0]['MAX(Id_Proyecto)'], ids = id)
              
     return render_template('Proyectos.html',datas = data,datas1 = data1,datasmats = valuepro,clientei = cliente)
@app.route('/output',methods=["GET","POST"])
def output():
    id = request.args.get('id-cot')
    data=db1.execute('SELECT * from Cotizacion where Id_Cotizacion = :idb',idb = id)
    Nombrecliente = db1.execute('select Nombre from Cliente,Cotizacion where Id_Cotizacion =:ids and Id_Cliente == IdCliente',ids = id)
    NC = Nombrecliente[0]['Nombre']
    descript = db1.execute('select  Nombre from DT_MProyect, MaterialProyecto where Id_Cot =:ids and Id_MP == Id_MaterialProyecto',ids = id)
    fp= datetime.now()
    fpss = datetime.strftime(fp,'%d-%m-%Y') 
    data1 = db1.execute('select sum (costo * Cantidad) totalmateriales from DT_MProyect where Id_Cot =:idsc',idsc = id)
    data2 = db1.execute('select sum (CostoMo * CantidadMo) as totalMo from Recursos WHERE IdCotizacion =:idsc1', idsc1 = id)
    datadescrip = db1.execute('SELECT Descripcion from Cotizacion where Id_Cotizacion =:ids',ids = id)
    dt = datadescrip[0]['Descripcion']
    datamt = data1[0]['totalmateriales']
    dtm  = int(datamt)
    dataMo = data2[0]['totalMo']
    dmo=int(dataMo)
    dataTotal = dtm + dmo
    datadescripfg =  db1.execute('select * from decripcionCot where Idcot=:ids',ids = id)
    return render_template('SCISApdfcot .html',nc = NC,ddescrip = descript,datadescrips = dt,date = fpss,datas1 = datamt,datas2 = dataMo,datas3 =dataTotal, datas = data ,fg= datadescripfg)  
           


#######################################################################
#Inicio del modulo rrhh para la vista del usuario
@ app.route('/RRHH')
def rrhh():
    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('RRHH.html', dias = vaca, di = di)

@ app.route('/rrhhmensaje')
def rrhhmensaje():
    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('RRHH.html', dias = vaca, di = di, salida = "correcto")

# Inicio de funciones para registrar las peticiones del modulo rrhh
@app.route('/prestaciones', methods=['GET', 'POST'])
def prestaciones():
    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        concepto = request.form["concepto"]
        cedula = request.form["cedula"]
        tipo = request.form['customRadio']

        f = request.files["archivo"]
        nombrear = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER2'], nombrear))

        today = date.today()

        con = "./templates/rrhhimg/" + nombrear

        if (tipo == "prestamo"):
            cuota = request.form["cuota"]
            montopr = request.form["montopr"]
            abono = request.form["pagar"]
            inicio = request.form["inicio"]
            final = request.form["final"]

            db1.execute('INSERT INTO prestaciones VALUES (null,:usu,:emp,:nom,:ape,:mon,:cuo,:con, :tip, :est, :ace, :ini, :fin, :mont, :fech, :const)',usu = session["user_Id"], emp = codigo, nom = nombre, ape = apellido, mon = montopr, cuo = cuota, con = concepto, tip = tipo, est = 6, ace = 2, ini =inicio, fin = final, mont = abono, fech = today, const = con)
        else:
            montoad = request.form["montoad"]
            db1.execute('INSERT INTO prestaciones VALUES (null,:usu,:emp,:nom,:ape,:mon, null,:con, :tip, :est, :ace, null, null, null, :fech, :const)',usu = session["user_Id"], emp = codigo, nom = nombre, ape = apellido, mon = montoad, con = concepto, tip = tipo, est = 6, ace = 2, fech = today, const = con)
            montoad = request.form["montoad"]

        return redirect(url_for('rrhhmensaje'))
    else:
        return redirect(url_for('/rrhh'))

@app.route('/vacaciones', methods=['GET', 'POST'])
def vacaciones():
    if request.method == "POST":
        codigo = request.form['codigo']
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        inicio = request.form["inicio"]
        final = request.form["final"]
        descripcion = request.form["descripcion"]
        motivo = request.form['marker']

        if (motivo == "otro"):
            motivo = request.form["mot"]

        fech1 = datetime.strptime(inicio, '%Y-%m-%d')
        fech2 = datetime.strptime(final, '%Y-%m-%d')
        d1 = fech1.date()
        d2 = fech2.date()

        delta = d2 - d1

        diasdevac = delta.days
        
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
        
        em = emp[0]["IdEmpleado"]

        dvaca = db1.execute(
        "Update Empleado Set diasvac = diasvac-:dias WHERE Id_Empleado =:emp", dias = diasdevac, emp = em)

        today = date.today()

        db1.execute('INSERT INTO vacaciones VALUES (null,:usu,:emp,:nom,:ape,:ini,:fin,:des, :mot, :est, :ace, :fec)',usu=session["user_Id"], emp = codigo, nom = nombre, ape = apellido, ini = inicio, fin = final, des = descripcion, mot = motivo, est = 1, ace = 2, fec = today)

        return redirect(url_for('rrhhmensaje'))
    else:
        return redirect(url_for('/rrhh'))

@app.route('/epp', methods=['GET', 'POST'])
def epp():
    if request.method == "POST":
        codigo = request.form['codigo']
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        equipo = request.form["equipo"]
        marca = request.form["marca"]
        cantidad = request.form["cantidad"]
        observacion = request.form["observacion"]
        tipo = request.form['customRadio']
        today = date.today()

        db1.execute('INSERT INTO epp VALUES (null,:usu,:emp,:nom,:ape,:equi,:mar,:can, :ob, :tip, :est, :ace, :fech)',usu=session["user_Id"], emp = codigo, nom = nombre, ape = apellido, equi = equipo, mar = marca, can = cantidad, ob = observacion, tip = tipo, est = 1, ace = 2, fech = today)

        return redirect(url_for('rrhhmensaje'))
    else:
        return redirect(url_for('/rrhh'))

@app.route('/viaticos', methods=['GET', 'POST'])
def viaticos():
    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        inicio = request.form["inicio"]
        final = request.form["final"]
        descripcion = request.form["descripcion"]
        destino = request.form["destino"]
        #motivo = request.form['marker']
        today = date.today()

        fech1 = datetime.strptime(inicio, '%Y-%m-%d')
        fech2 = datetime.strptime(final, '%Y-%m-%d')
        d1 = fech1.date()
        d2 = fech2.date()

        dias = d2 - d1

        print("el valor de dias es:", dias)
        totaldias = dias.days + 1

        print("El total de dias es: ", totaldias)

        #if (motivo == "otro"):
        #    motivo = request.form["mot"]
        
        conceptos = request.form.getlist('conceptos[]')
        montos = request.form.getlist('montos[]')

        tam = len(conceptos)

        db1.execute('INSERT INTO viaticos VALUES (null,:usu,:emp,:nom,:ape,:ini,:fin,:des, :dest, :est, :ace, :fec)',usu=session["user_Id"], emp = codigo, nom = nombre, ape = apellido, ini = inicio, fin = final, des = descripcion, dest = destino, est = 1, ace = 2, fec = today)

        proximo = db1.execute(
        "select idviatico from viaticos ORDER BY idviatico DESC LIMIT 1")

        next = proximo[0]["idviatico"]

        IdDetalleViatico = next

        for i in range(tam):
            db1.execute('INSERT INTO DetalleViatico VALUES (null,:idvia,:con,:mon, :subtotal)', idvia = IdDetalleViatico, con = conceptos[i], mon = montos[i], subtotal = (float(montos[i]) * totaldias))

        #db1.execute('INSERT INTO viaticos VALUES (null,:usu,:emp,:nom,:ape,:ini,:fin,:des, :dest, :mot, :est, :ace, :fec)',usu=session["user_Id"], emp = codigo, nom = nombre, ape = apellido, ini = inicio, fin = final, des = descripcion, dest = destino, mot = motivo, est = 1, ace = 2, fec = today)

        return redirect(url_for('rrhhmensaje'))
    else:
        return redirect(url_for('/rrhh'))

# Inicio de funciones para buscar por codigo en cada una de las pestañas de prestaciones y retornar el html con el form correspondiente
@app.route('/busquedacodpre', methods=['POST'])
def busquedacodpre():
    codigo = request.form["codigo"]

    salida = db1.execute(
     "select Id_Empleado, salario, Nombre, Apellido, Cedula from Empleado WHERE Id_Empleado =:emp", emp = codigo)
    
    if not(salida):
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days
        
        return render_template('RRHH.html', dias = vaca, di = di, salida = "noencontrado", info = salida)
    else:
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days

        return render_template('/Rrhh/busqueda/RRHHbusquedapres.html', dias = vaca, di = di, salida = "encontrado", info = salida)

@app.route('/busquedacodvac', methods=['POST'])
def busquedacodvac():
    codigo = request.form["codigo"]

    salida = db1.execute(
     "select Id_Empleado, salario, Nombre, Apellido, Cedula from Empleado WHERE Id_Empleado =:emp", emp = codigo)
    
    if not(salida):
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days
        
        return render_template('RRHH.html', dias = vaca, di = di, salida = "noencontrado", info = salida)
    else:
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days

        return render_template('/Rrhh/busqueda/RRHHbusquedavac.html', dias = vaca, di = di, salida = "encontrado", info = salida)

@app.route('/busquedacodepp', methods=['POST'])
def busquedacodepp():
    codigo = request.form["codigo"]

    salida = db1.execute(
     "select Id_Empleado, salario, Nombre, Apellido, Cedula from Empleado WHERE Id_Empleado =:emp", emp = codigo)
    
    if not(salida):
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days
        
        return render_template('RRHH.html', dias = vaca, di = di, salida = "noencontrado", info = salida)
    else:
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days

        return render_template('/Rrhh/busqueda/RRHHbusquedaepp.html', dias = vaca, di = di, salida = "encontrado", info = salida)

@app.route('/busquedacodvia', methods=['POST'])
def busquedacodvia():
    codigo = request.form["codigo"]

    salida = db1.execute(
     "select Id_Empleado, salario, Nombre, Apellido, Cedula from Empleado WHERE Id_Empleado =:emp", emp = codigo)
    
    if not(salida):
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days
        
        return render_template('RRHH.html', dias = vaca, di = di, salida = "noencontrado", info = salida)
    else:
        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        vaca = db1.execute(
            "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

        d = vaca[0]["fechacontrato"]

        fech1 = datetime.strptime(d, '%Y-%m-%d')
        d1 = fech1.date()
        today = date.today()

        delta = today - d1

        di = delta.days

        return render_template('/Rrhh/busqueda/RRHHbusquedavia.html', dias = vaca, di = di, salida = "encontrado", info = salida)

#Inicio de las funciones para mostrar las solicitudess
@app.route('/mostrarprestaciones', methods=['GET', 'POST'])
def mostrarprestaciones():
    presta = db1.execute(
        "select idprestacion, concepto, tipo, Monto, aceptado from prestaciones WHERE IdUsuario =:user", user = session["user_Id"])

    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('/Rrhh/prestaciones.html', dias = vaca, di = di, presta = presta)

@app.route('/mostrarvacaciones', methods=['GET', 'POST'])
def mostrarvacaciones():
    presta = db1.execute(
        "select idvacaciones, descripcion, motivo, fecha, aceptado from vacaciones WHERE IdUsuario =:user", user = session["user_Id"])
    
    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('/Rrhh/vacaciones.html', dias = vaca, di = di, presta = presta)

@app.route('/mostrarepp', methods=['GET', 'POST'])
def mostrarepp():
    presta = db1.execute(
        "select idepp, equipo, marca, cantidad, aceptado from epp WHERE IdUsuario =:user", user = session["user_Id"])
    
    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('/Rrhh/epp.html', dias = vaca, di = di, presta = presta)

@app.route('/mostrarviaticos', methods=['GET', 'POST'])
def mostrarviaticos():
    presta = db1.execute(
        "select idviatico, idviatico, inicio, final, destino, aceptado from viaticos WHERE IdUsuario =:user", user = session["user_Id"])
    
    emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])
    em = emp[0]["IdEmpleado"]
        
    vaca = db1.execute(
        "select diasvac, salario, fechacontrato from Empleado WHERE Id_Empleado =:e", e = em)

    d = vaca[0]["fechacontrato"]

    fech1 = datetime.strptime(d, '%Y-%m-%d')
    d1 = fech1.date()
    today = date.today()

    delta = today - d1

    di = delta.days
       
    return render_template('/Rrhh/viaticos.html', dias = vaca, di = di, presta = presta)

# Inicio de las funciones para mostrar las solicitudes
@app.route("/infoprestaciones/<int:id>", methods=['GET', 'POST'])
def infoprestaciones(id):
    if request.method == "POST":
        img = db1.execute(
        "select constancia from prestaciones WHERE idprestacion =:i", i = id)

        salida = db1.execute(
        "delete from prestaciones WHERE idprestacion =:i", i = id)

        imagen = img[0]["constancia"]
        print("esto contiene img: ", img)

        remove(imagen)

        return redirect(url_for( 'mostrarprestaciones'))
    else:
        presta = db1.execute(
        "select * from prestaciones WHERE idprestacion =:i", i = id)

        emp = db1.execute(
        "select IdEmpleado from Usuario WHERE Id_Usuario =:user", user = session["user_Id"])

        em = emp[0]["IdEmpleado"]
            
        sal = db1.execute(
            "select salario from Empleado WHERE Id_Empleado =:e", e = em)

        d = sal[0]["salario"]

        return render_template('/Rrhh/mostrar/verprestaciones.html', info = presta, sal = d)

@app.route("/infovacaciones/<int:id>", methods=['GET', 'POST'])
def infovacaciones(id):
    if request.method == "POST":
        sal = db1.execute(
            "delete from vacaciones WHERE idvacaciones = :id", id = id)

        return redirect(url_for( 'mostrarvacaciones'))
    else:
        presta = db1.execute(
            "select * from vacaciones WHERE idvacaciones =:i", i = id)

        return render_template('/Rrhh/mostrar/vervacacion.html', info = presta)

@app.route("/infoepp/<int:id>", methods=['GET', 'POST'])
def infoepp(id):
    if request.method == "POST":
        sal = db1.execute(
            "delete from epp WHERE idepp = :id", id = id)

        return redirect(url_for( 'mostrarepp'))
    else:
        presta = db1.execute(
            "select * from epp WHERE idepp =:i", i = id)

        return render_template('/Rrhh/mostrar/verepp.html', info = presta)

@app.route("/infoviaticos/<int:id>", methods=['GET', 'POST'])
def infoviaticos(id):
    if request.method == "POST":
        sal1 = db1.execute(
            "delete from DetalleViatico WHERE idviatico = :id", id = id)
        
        sal = db1.execute(
            "delete from viaticos WHERE idviatico = :id", id = id)

        return redirect(url_for( 'mostrarviaticos'))
    else:
        presta = db1.execute(
            "select * from viaticos WHERE idviatico =:i", i = id)

        id = presta[0]["idviatico"]

        det = db1.execute(
            "select * from DetalleViatico WHERE idviatico =:id", id = id)

        tot = db1.execute("select sum(subtotal) as tot from DetalleViatico WHERE idviatico =:id", id = id)

        total = tot[0]["tot"]

        return render_template('/Rrhh/mostrar/verviaticos.html', info = presta, detalle = det, total = total)

# Inicio de funciones de actualizar datos de prestaciones
@app.route("/actualizarprestacion", methods=['POST'])
def actualizarprestacion():
    if request.method == "POST":
        tipo = request.form['customRadio']
        id = request.form['id']
        today = date.today()

        if (tipo == "prestamo"):
            monto = request.form["montopr"]
            cuota = request.form["cuota"]
            concepto = request.form["concepto"]
            inicio = request.form["inicio"]
            final = request.form["final"]
            montopago = request.form["pagar"]
        
            db1.execute('UPDATE  prestaciones SET Monto = :mon, cuotas = :cuo, concepto = :con, inicio = :ini, final = :fin, montopago = :mp, fecha = :fec WHERE idprestacion = :id',
                mon = monto, cuo = cuota, con = concepto, ini = inicio, fin = final, mp = montopago, fec = today, id = id)

        elif (tipo == "adelanto"):
            monto = request.form["montoad"]
            concepto = request.form["concepto"]

            db1.execute('UPDATE  prestaciones SET Monto = :mon, concepto = :con, fecha = :fec WHERE idprestacion = :id',
                mon = monto, con = concepto, fec = today, id = id)

        return redirect(url_for( 'mostrarprestaciones'))

########################################################################
#Inicio de funciones del menu del admin
@app.route("/RRHHadmin", methods=['GET','POST'])
def RRHHadmin():
#    mayo = db1.execute(
 #       "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-05-01' AND '2022-05-31' ")
#    junio = db1.execute(
   #     "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-06-01' AND '2022-06-31' ")

    #return render_template("RRHHadmin.html", jun = junio, may = mayo)
    return render_template("RRHHadmin.html")

#@app.route("/verprestacionesempleado/<int:id>", methods=['GET','POST'])
#def verprestacionesempleado(id):
#    emp = db1.execute(
#        "select Id_Empleado, Nombre, Apellido from Empleado")

#    info = db1.execute(
#        "select idprestacion, concepto, tipo, Monto, aceptado from prestaciones where Id_Empleado = :emp", emp = id)

#    return render_template("/Rrhh/admin/prestacionesadmin.html", emp = emp, info = info)
#@app.route("/vervacacionesempleado/<int:id>", methods=['GET','POST'])
#def vervacacionesempleado(id):
#    emp = db1.execute(
 #       "select Id_Empleado, Nombre, Apellido from Empleado")

  #  info = db1.execute(
   #     "select descripcion, motivo, fecha, aceptado from vacaciones where Id_Empleado = :emp", emp = id)

    #return render_template("/Rrhh/admin/vacacionesadmin.html", emp = emp, info = info)

#@app.route("/vereppempleado/<int:id>", methods=['GET','POST'])
#def vereppempleado(id):
 #   emp = db1.execute(
  #      "select Id_Empleado, Nombre, Apellido from Empleado")

   # info = db1.execute(
    #    "select equipo, marca, cantidad, aceptado from epp where Id_Empleado = :emp", emp = id)

    #return render_template("/Rrhh/admin/eppadmin.html", emp = emp, info = info)

#@app.route("/verviaticosempleado/<int:id>", methods=['GET','POST'])
#def verviaticosempleado(id):
 #   emp = db1.execute(
  #      "select Id_Empleado, Nombre, Apellido from Empleado")

   # info = db1.execute(
    #    "select inicio, final, destino, aceptado from viaticos where Id_Empleado = :emp", emp = id)

    #return render_template("/Rrhh/admin/viaticosadmin.html", emp = emp, info = info)

@app.route("/prueba", methods=['GET','POST'])
def prueba():
    if request.method == "POST":
        conceptos = request.form.getlist('conceptos[]')
        montos = request.form.getlist('montos[]')

        tam = len(conceptos)

        for i in range(tam):
            db1.execute('INSERT INTO DetalleViatico VALUES (null,:usu,:emp,:nom,:ape,:ini,:fin,:des, :dest, :mot, :est, :ace, :fec)',usu=session["user_Id"], emp = codigo, nom = nombre, ape = apellido, ini = inicio, fin = final, des = descripcion, dest = destino, mot = motivo, est = 1, ace = 2, fec = today)

        print("Conceptos vale: ", conceptos)

        return conceptos[1]
    else:
        return "metodo get"

#Acá inician las funciones de busqueda y filtros del admin
@app.route("/busqueda",methods=["POST"])
def busqueda():
    me = int(request.form['mes'])
    tipo = int(request.form['tip'])

    mes = {}
    #Mi variable mes controla el numero del mes del año a buscar
    #Mi variable tipo controla el tipo de solicitud, ya sea epp, viatico, etc

    if(me == 1):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-01-01' AND '2022-01-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-01-01' AND '2022-01-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-01-01' AND '2022-01-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-01-01' AND '2022-01-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 2):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-02-01' AND '2022-02-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-02-01' AND '2022-02-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-02-01' AND '2022-02-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-02-01' AND '2022-02-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 3):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-03-01' AND '2022-03-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-03-01' AND '2022-03-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-03-01' AND '2022-03-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-03-01' AND '2022-03-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})
    elif(me == 4):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-04-01' AND '2022-04-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-04-01' AND '2022-04-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-04-01' AND '2022-04-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-04-01' AND '2022-04-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 5):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-05-01' AND '2022-05-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-05-01' AND '2022-05-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-05-01' AND '2022-05-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-05-01' AND '2022-05-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 6):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-06-01' AND '2022-06-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-06-01' AND '2022-06-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-06-01' AND '2022-06-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-06-01' AND '2022-06-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 7):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-07-01' AND '2022-07-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-07-01' AND '2022-07-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-07-01' AND '2022-07-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-07-01' AND '2022-07-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 8):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-08-01' AND '2022-08-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-08-01' AND '2022-08-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-08-01' AND '2022-08-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-08-01' AND '2022-08-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 9):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-09-01' AND '2022-09-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-09-01' AND '2022-09-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-09-01' AND '2022-09-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-09-01' AND '2022-09-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 10):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-10-01' AND '2022-10-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-10-01' AND '2022-10-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-10-01' AND '2022-10-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-10-01' AND '2022-10-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 11):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-11-01' AND '2022-11-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-11-01' AND '2022-11-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-11-01' AND '2022-11-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-11-01' AND '2022-11-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

    elif(me == 12):
        if (tipo == 1):
            mes = db1.execute(
                "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between '2022-12-01' AND '2022-12-31' ")
        
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verprestacionadmin.html', m = mes)})

        elif (tipo == 2):
            mes = db1.execute(
                "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between '2022-12-01' AND '2022-12-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vervacacionesadmin.html', m = mes)})
        elif (tipo == 3):
            mes = db1.execute(
                "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between '2022-12-01' AND '2022-12-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/vereppadmin.html', m = mes)})

        elif (tipo == 4):
            mes = db1.execute(
                "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between '2022-12-01' AND '2022-12-31' ")
            
            return jsonify({'htmlresponse': render_template('/rrhhadmin/verviaticosadmin.html', m = mes)})

@app.route('/filtro', methods=['POST'])
def filtro():
    pet = int(request.form['pet'])
    tipo = int(request.form['tip'])

    presta = {}
    enzabesado = ""
    ay = ""
    to = ""

    today = date.today()

    if (today.month < 10):
        ay = '0' + str(today.month)
    else:
        ay = today.month

    if (today.day < 10):
        d = today.day - 1
        to = '0' + str(d)
    else:
        to = today.day - 1

    ayer = str(today.year) + '-' + str(ay) + '-' + str(to)

    inicio = str(today.year) + '-' + str(ay) + '-' + '01'
    #print("incio vale: ", inicio)
    final = str(today.year) + '-' + str(ay) + '-' + '31'

    if (pet == 1):
        if (tipo == 1):
            enzabesado = "Solicitudes de prestaciones de hoy"

            presta = db1.execute(
        "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha = :t", t = today)
       
            return render_template('/rrhhadmin/filtro/prestacionesfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 2):
            enzabesado = "Solicitudes de vacaciones de hoy"

            presta = db1.execute(
        "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha = :t", t = today)
       
            return render_template('/rrhhadmin/filtro/vacacionesfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 3):
            enzabesado = "Solicitudes de epp de hoy"

            presta = db1.execute(
        "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha = :t", t = today)
       
            return render_template('/rrhhadmin/filtro/eppfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 4):
            enzabesado = "Solicitudes de viaticos de hoy"

            presta = db1.execute(
        "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha = :t ", t = today)
       
            return render_template('/rrhhadmin/filtro/viaticosfiltro.html', presta = presta, encabezado = enzabesado)

    elif (pet == 2):
        if (tipo == 1):
            enzabesado = "Solicitudes de prestaciones de ayer"

            presta = db1.execute(
        "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha = :t", t = ayer)
       
            return render_template('/rrhhadmin/filtro/prestacionesfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 2):
            enzabesado = "Solicitudes de vacaciones de ayer"

            presta = db1.execute(
        "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha = :t", t = ayer)
       
            return render_template('/rrhhadmin/filtro/vacacionesfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 3):
            enzabesado = "Solicitudes de epp de ayer"

            presta = db1.execute(
        "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha = :t", t = ayer)
       
            return render_template('/rrhhadmin/filtro/eppfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 4):
            enzabesado = "Solicitudes de viaticos de ayer"

            presta = db1.execute(
        "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha = :t ", t = ayer)
       
            return render_template('/rrhhadmin/filtro/viaticosfiltro.html', presta = presta, encabezado = enzabesado)

    elif (pet == 3):
        if (tipo == 1):
            enzabesado = "Solicitudes de prestaciones del mes"

            presta = db1.execute(
        "select idprestacion, Nombres, Apellidos, Monto, tipo, aceptado from prestaciones where fecha between :t1 AND :t2 ", t1 = inicio, t2 = final)
       
            return render_template('/rrhhadmin/filtro/prestacionesfiltro.html', presta = presta, encabezado = enzabesado)
        elif (tipo == 2):
            enzabesado = "Solicitudes de vacaciones del mes"

            presta = db1.execute(
        "select idvacaciones, nombres, apellidos, inicio, final, aceptado from vacaciones where fecha between :t1 AND :t2 ", t1 = inicio, t2 = final)
       
            return render_template('/rrhhadmin/filtro/vacacionesfiltro.html', presta = presta, encabezado = enzabesado)

        elif (tipo == 3):
            enzabesado = "Solicitudes de epp del mes"

            presta = db1.execute(
        "select idepp, nombres, apellidos, equipo, cantidad, aceptado from epp where fecha between :t1 AND :t2 ", t1 = inicio, t2 = final)
       
            return render_template('/rrhhadmin/filtro/eppfiltro.html', presta = presta, encabezado = enzabesado)
        elif (tipo == 4):
            enzabesado = "Solicitudes de viaticos del mes"

            presta = db1.execute(
        "select idviatico, nombres, apellidos, inicio, final, aceptado from viaticos where fecha between :t1 AND :t2 ", t1 = inicio, t2 = final)
       
            return render_template('/rrhhadmin/filtro/viaticosfiltro.html', presta = presta, encabezado = enzabesado)

@app.route("/verprestacionesempleado/<int:id>", methods=['GET','POST'])
def verprestacionesempleado(id):
    if request.method == "POST":
        id = int(request.form["id"])
        aceptado = int(request.form["aceptado"])

        ac = 0

        print("aceptado vale: ", aceptado)

        if (aceptado == 2):
            ac = 1
        elif (aceptado == 1):
            ac = 0

        db1.execute(
        "Update prestaciones Set aceptado = :ac WHERE idprestacion = :id", ac = ac, id = id)

        return redirect(url_for('RRHHadmin'))
    else:
        presta = db1.execute(
            "select * from prestaciones WHERE idprestacion =:i", i = id)

        return render_template('/rrhhadmin/veradmin/aceptarprestacion.html', info = presta)

@app.route("/vervacacionesempleado/<int:id>", methods=['GET','POST'])
def vervacacionesempleado(id):
    if request.method == "POST":
        id = int(request.form["id"])
        aceptado = int(request.form["aceptado"])

        ac = 0

        print("aceptado vale: ", aceptado)

        if (aceptado == 2):
            ac = 1
        elif (aceptado == 1):
            ac = 0

        db1.execute(
        "Update vacaciones Set aceptado = :ac WHERE idvacaciones = :id", ac = ac, id = id)

        return redirect(url_for('RRHHadmin'))
    else:
        presta = db1.execute(
            "select * from vacaciones WHERE idvacaciones =:i", i = id)

        return render_template('/rrhhadmin/veradmin/aceptarvacacion.html', info = presta)

@app.route("/vereppempleado/<int:id>", methods=['GET','POST'])
def vereppempleado(id):
    if request.method == "POST":
        id = int(request.form["id"])
        aceptado = int(request.form["aceptado"])

        ac = 0

        print("aceptado vale: ", aceptado)

        if (aceptado == 2):
            ac = 1
        elif (aceptado == 1):
            ac = 0

        db1.execute(
        "Update epp Set aceptado = :ac WHERE idepp = :id", ac = ac, id = id)

        return redirect(url_for('RRHHadmin'))
    else:
        presta = db1.execute(
            "select * from epp WHERE idepp =:i", i = id)

        return render_template('/rrhhadmin/veradmin/aceptarepp.html', info = presta)

@app.route("/verviaticoempleado/<int:id>", methods=['GET','POST'])
def verviaticoempleado(id):
    if request.method == "POST":
        id = int(request.form["id"])
        aceptado = int(request.form["aceptado"])

        ac = 0

        print("aceptado vale: ", aceptado)

        if (aceptado == 2):
            ac = 1
        elif (aceptado == 1):
            ac = 0

        db1.execute(
        "Update viaticos Set aceptado = :ac WHERE idviatico = :id", ac = ac, id = id)

        return redirect(url_for('RRHHadmin'))
    else:
        presta = db1.execute(
            "select * from viaticos WHERE idviatico =:i", i = id)

        id = presta[0]["idviatico"]

        det = db1.execute(
            "select * from DetalleViatico WHERE idviatico =:id", id = id)

        tot = db1.execute("select sum(subtotal) as tot from DetalleViatico WHERE idviatico =:id", id = id)

        total = tot[0]["tot"]

        return render_template('/rrhhadmin/veradmin/aceptarviatico.html', info = presta, detalle = det, total = total)

def errorhandler(e):
    return render_template("error.html", nombre = e.name, codigo = e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
