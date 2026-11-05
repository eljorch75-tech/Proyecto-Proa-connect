const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();


// ============================================================
// INICIAR SESIÓN
// POST /login
// ============================================================

router.post("/", async (req, res) => {

    const { nombre_usuario, contrasena } = req.body;


    // Verificar que se hayan enviado usuario y contraseña
    if (!nombre_usuario || !contrasena) {

        return res.status(400).json({
            error: "Debe ingresar usuario y contraseña"
        });

    }


    try {

        // Buscar el usuario en la base de datos
        const [usuarios] = await pool.query(
            `SELECT *
             FROM usuario
             WHERE nombre_usuario = ?`,
            [nombre_usuario]
        );


        // Si no existe
        if (usuarios.length === 0) {

            return res.status(401).json({
                error: "Usuario o contraseña incorrectos"
            });

        }


        const usuario = usuarios[0];


        // ====================================================
        // VERIFICAR CONTRASEÑA
        // ====================================================

        if (usuario.contrasena !== contrasena) {

            return res.status(401).json({
                error: "Usuario o contraseña incorrectos"
            });

        }


        // ====================================================
        // INICIO DE SESIÓN CORRECTO
        // ====================================================

        return res.status(200).json({

            mensaje: "Inicio de sesión correcto",

            id_usuario: usuario.id_usuario,

            nombre_usuario: usuario.nombre_usuario,

            id_docente: usuario.id_docente

        });

    } catch (error) {

        console.log("Error al iniciar sesión:", error);

        return res.status(500).json({
            error: "Error al validar el usuario"
        });

    }

});


module.exports = router;
