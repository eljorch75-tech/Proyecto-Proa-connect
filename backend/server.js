const express = require("express");
const pool = require("./bd/conexion")
const estudiantesRouter = require("./rutas/estudiantes")
const loginRouter = require("./rutas/login")
const asistenciaRouter = require("./rutas/asistencia")

const app = express();
const PORT = 3000;

app.use(express.json());

app.use("/api/estudiantes", estudiantesRouter);
app.use("/api/login", loginRouter)
app.use("/api/asistencia", asistenciaRouter)
async function probarConexion() {
 try {
    await pool.query ("SELECT 1");
    console.log("conexion exitosa")
 } catch (error) {
     console.log("Error en la conexion")
     console.log(error.message)
 }   
}
console.log("antes");

app.listen(PORT, async() => {
    console.log(`servidor ejecutándose en http://localhost:${PORT}`);
    await probarConexion()
});
