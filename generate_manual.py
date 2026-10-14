# -*- coding: utf-8 -*-
"""
Generador Maestro del Manual y Guía de Laboratorio de Sistemas Distribuidos
(Práctica 2 - gRPC en .NET 10 para 3º Grado en Ingeniería Informática)
"""

import os
import sys
import subprocess
import html
import pygments
from pygments.lexers import CSharpLexer, ProtoBufLexer, XmlLexer, BashLexer, PowerShellLexer
from pygments.formatters import HtmlFormatter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def highlight_code(code_str, lexer_type):
    lexers = {
        "csharp": CSharpLexer(),
        "proto": ProtoBufLexer(),
        "xml": XmlLexer(),
        "bash": BashLexer(),
        "powershell": PowerShellLexer()
    }
    lexer = lexers.get(lexer_type, CSharpLexer())
    formatter = HtmlFormatter(noclasses=True, style='github-dark')
    return pygments.highlight(code_str, lexer, formatter)

def code_block_html(title, filename, lang, code_str, allow_break=False):
    highlighted = highlight_code(code_str, lang)
    break_class = "" if allow_break else "avoid-break"
    return f"""
    <div class="code-card {break_class}">
        <div class="code-header">
            <span class="code-filename"><span class="code-icon">📄</span> <strong>{filename}</strong> &nbsp;—&nbsp; <small style="color:#94a3b8;">{title}</small></span>
            <span class="code-lang-badge">{lang.upper()}</span>
        </div>
        <div class="code-body">
            {highlighted}
        </div>
    </div>
    """

def callout(box_type, title, content):
    icons = {
        "exam": "🎓",
        "why": "💡",
        "warning": "⚠️",
        "step": "🛠️",
        "example": "🔍"
    }
    classes = {
        "exam": "callout-exam",
        "why": "callout-why",
        "warning": "callout-warning",
        "step": "callout-step",
        "example": "callout-example"
    }
    icon = icons.get(box_type, "📌")
    css_class = classes.get(box_type, "callout-why")
    return f"""
    <div class="callout {css_class} avoid-break">
        <div class="callout-title">{icon} {title}</div>
        <div class="callout-body">{content}</div>
    </div>
    """

# Cargar archivos reales
proto_code = read_file("Protos/restaurante.proto")
rest_proj = read_file("Restaurante/Restaurante.csproj")
rest_pedido = read_file("Restaurante/Pedido.cs")
rest_prog = read_file("Restaurante/Program.cs")
rest_service = read_file("Restaurante/RestauranteService.cs")
rep_proj = read_file("Repartidor/Repartidor.csproj")
rep_prog = read_file("Repartidor/Program.cs")
cli_proj = read_file("Cliente/Cliente.csproj")
cli_service = read_file("Cliente/RestauranteClienteService.cs")
cli_prog = read_file("Cliente/Program.cs")
slnx_code = read_file("SistemaRestaurante.slnx")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Sistemas Distribuidos - Práctica 2: Sistema de Restaurante con gRPC en .NET 10</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 16mm 14mm 16mm 14mm;
        @bottom-right {{
            content: "Página " counter(page);
            font-size: 8pt;
            color: #64748b;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        @bottom-left {{
            content: "Sistemas Distribuidos (3º Grado Ing. Informática) · Práctica 2: gRPC en .NET 10";
            font-size: 8pt;
            color: #64748b;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
    }}

    @page :first {{
        margin-top: 0;
        @bottom-right {{ content: none; }}
        @bottom-left {{ content: none; }}
    }}

    @media print {{
        body {{
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        .avoid-break {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
    }}

    * {{
        box-sizing: border-box;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 9.3pt;
        line-height: 1.5;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}

    /* Portada Premium */
    .cover {{
        padding: 40px 10px 10px 10px;
        min-height: 92vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
    }}

    .cover-top {{
        border-bottom: 3px solid #2563eb;
        padding-bottom: 25px;
        margin-bottom: 25px;
    }}

    .cover-badge {{
        display: inline-block;
        background: #1e3a8a;
        color: #ffffff;
        font-size: 9.5pt;
        font-weight: 700;
        padding: 6px 18px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 18px;
    }}

    .cover-title {{
        font-size: 27pt;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.15;
        margin: 0 0 12px 0;
        letter-spacing: -0.6px;
    }}

    .cover-subtitle {{
        font-size: 13pt;
        font-weight: 500;
        color: #334155;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.4;
    }}

    .cover-card {{
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 12px;
        padding: 22px 28px;
        text-align: left;
        max-width: 580px;
        margin: 20px auto;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}

    .cover-card-grid {{
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 9px 18px;
        font-size: 9pt;
    }}

    .cover-card-label {{
        font-weight: 700;
        color: #1e3a8a;
    }}

    .cover-card-val {{
        color: #0f172a;
        font-weight: 500;
    }}

    .cover-footer {{
        border-top: 1px solid #e2e8f0;
        padding-top: 14px;
        font-size: 8.5pt;
        color: #64748b;
        margin-top: 20px;
    }}

    /* Encabezados */
    h1 {{
        font-size: 16.5pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2.5px solid #2563eb;
        padding-bottom: 5px;
        margin-top: 22px;
        margin-bottom: 12px;
        letter-spacing: -0.3px;
        break-after: avoid;
    }}

    h2 {{
        font-size: 12.5pt;
        font-weight: 700;
        color: #1e3a8a;
        margin-top: 18px;
        margin-bottom: 8px;
        border-left: 4px solid #3b82f6;
        padding-left: 8px;
        break-after: avoid;
    }}

    h3 {{
        font-size: 10pt;
        font-weight: 700;
        color: #334155;
        margin-top: 14px;
        margin-bottom: 6px;
        break-after: avoid;
    }}

    p {{
        margin-top: 0;
        margin-bottom: 8px;
        text-align: justify;
    }}

    ul, ol {{
        margin-top: 0;
        margin-bottom: 8px;
        padding-left: 18px;
    }}

    li {{
        margin-bottom: 3px;
    }}

    /* Tablas */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 8.5pt;
    }}

    th, td {{
        border: 1px solid #cbd5e1;
        padding: 6px 9px;
        text-align: left;
    }}

    th {{
        background: #1e293b;
        color: #ffffff;
        font-weight: 600;
    }}

    tr:nth-child(even) {{
        background: #f8fafc;
    }}

    /* Callouts */
    .callout {{
        border-radius: 8px;
        padding: 10px 14px;
        margin: 12px 0;
        font-size: 8.8pt;
        border-left: 5px solid;
    }}

    .callout-title {{
        font-weight: 700;
        margin-bottom: 4px;
        font-size: 9.3pt;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .callout-body p:last-child {{
        margin-bottom: 0;
    }}

    .callout-exam {{
        background-color: #fffbeb;
        border-left-color: #d97706;
        color: #78350f;
    }}
    .callout-exam .callout-title {{
        color: #92400e;
    }}

    .callout-why {{
        background-color: #eff6ff;
        border-left-color: #2563eb;
        color: #1e3a8a;
    }}
    .callout-why .callout-title {{
        color: #1d4ed8;
    }}

    .callout-warning {{
        background-color: #fff1f2;
        border-left-color: #e11d48;
        color: #881337;
    }}
    .callout-warning .callout-title {{
        color: #be123c;
    }}

    .callout-step {{
        background-color: #ecfdf5;
        border-left-color: #059669;
        color: #064e3b;
    }}
    .callout-step .callout-title {{
        color: #047857;
    }}

    .callout-example {{
        background-color: #f5f3ff;
        border-left-color: #7c3aed;
        color: #4c1d95;
    }}
    .callout-example .callout-title {{
        color: #6d28d9;
    }}

    /* Código */
    .code-card {{
        border: 1px solid #334155;
        border-radius: 7px;
        margin: 12px 0;
        background: #0d1117;
    }}

    .code-header {{
        background: #161b22;
        padding: 5px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #30363d;
        font-size: 8pt;
        color: #c9d1d9;
        font-weight: 600;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }}

    .code-lang-badge {{
        background: #238636;
        color: #ffffff;
        font-size: 6.8pt;
        font-weight: 700;
        padding: 1px 5px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }}

    .code-body {{
        padding: 7px 12px;
        overflow-x: auto;
    }}

    .code-body pre {{
        margin: 0;
        font-family: "Cascadia Code", "Fira Code", Consolas, "Courier New", monospace !important;
        font-size: 7.7pt !important;
        line-height: 1.38 !important;
        background: transparent !important;
    }}

    code.inline {{
        font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
        background: #f1f5f9;
        color: #0f172a;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 8.2pt;
        border: 1px solid #e2e8f0;
    }}

    /* Diagramas SVG */
    .diagram-container {{
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px;
        margin: 12px 0;
        text-align: center;
    }}

    .diagram-caption {{
        font-size: 8pt;
        font-weight: 600;
        color: #475569;
        margin-top: 6px;
    }}

    /* Tabla de contenidos */
    .toc {{
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 16px 0;
    }}
    .toc-title {{
        font-size: 10.5pt;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 4px;
    }}
    .toc-list {{
        list-style: none;
        padding-left: 0;
        margin: 0;
        font-size: 8.8pt;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px 16px;
    }}
    .toc-list li {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px;
    }}
    .toc-item-num {{
        font-weight: 700;
        color: #2563eb;
        margin-right: 5px;
    }}
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover">
    <div class="cover-top">
        <div class="cover-badge">Grado en Ingeniería Informática · 3.er Curso</div>
        <h1 class="cover-title">SISTEMAS DISTRIBUIDOS<br>PRÁCTICA 2: gRPC EN .NET 10</h1>
        <div class="cover-subtitle">
            Guía Integral de Principio a Fin: Diseño de IDL, Concurrencia Multihilo en Memoria y Arquitectura Distribuida con C#
        </div>
    </div>

    <div class="cover-card">
        <div class="cover-card-grid">
            <div class="cover-card-label">Asignatura:</div>
            <div class="cover-card-val">Sistemas Distribuidos / Computación Distribuida</div>
            
            <div class="cover-card-label">Ámbito Académico:</div>
            <div class="cover-card-val">Escuela Técnica Superior de Ingeniería Informática (España)</div>

            <div class="cover-card-label">Plataforma & Lenguaje:</div>
            <div class="cover-card-val">.NET 10.0 SDK & C# 13</div>

            <div class="cover-card-label">Middleware / IPC:</div>
            <div class="cover-card-val">gRPC (Google Remote Procedure Call) sobre HTTP/2 (h2c)</div>

            <div class="cover-card-label">Formato de Contrato:</div>
            <div class="cover-card-val">Protocol Buffers v3 (proto3 IDL)</div>

            <div class="cover-card-label">Patrón Concurrente:</div>
            <div class="cover-card-val">Productor-Consumidor con Búfer Acotado en Memoria</div>

            <div class="cover-card-label">Sincronización:</div>
            <div class="cover-card-val">SemaphoreSlim, ConcurrentQueue, ConcurrentDictionary, lock</div>
        </div>
    </div>

    <div class="cover-footer">
        <strong>Manual Oficial de Prácticas y Guía de Defensa de Examen</strong><br>
        Documento estructurado con rigor teórico-práctico para dominar la implementación paso a paso y responder con excelencia en la evaluación oral.
    </div>
</div>

<div class="page-break"></div>

<!-- ÍNDICE DE CONTENIDOS -->
<div class="toc avoid-break">
    <div class="toc-title">📋 Índice General de Contenidos</div>
    <ul class="toc-list">
        <li><span><span class="toc-item-num">1.</span> Fundamentos Teóricos de Sistemas Distribuidos</span></li>
        <li><span><span class="toc-item-num">2.</span> Arquitectura Global del Sistema</span></li>
        <li><span><span class="toc-item-num">3.</span> Construcción del Proyecto Desde Cero (CLI)</span></li>
        <li><span><span class="toc-item-num">4.</span> El Contrato de Comunicación (IDL Protobuf)</span></li>
        <li><span><span class="toc-item-num">5.</span> Configuración de los Proyectos (.csproj)</span></li>
        <li><span><span class="toc-item-num">6.</span> El Servidor (Restaurante): Concurrencia y Estado</span></li>
        <li><span><span class="toc-item-num">7.</span> El Agente Consumidor (Repartidor): Worker Loop</span></li>
        <li><span><span class="toc-item-num">8.</span> La Aplicación Cliente (Cliente): Menú y Stubs</span></li>
        <li><span><span class="toc-item-num">9.</span> Guía de Ejecución y Casos de Prueba Límite</span></li>
        <li><span><span class="toc-item-num">10.</span> Banco de 10 Preguntas Típicas de Examen</span></li>
        <li><span><span class="toc-item-num">11.</span> Chuleta de Depuración y Resolución de Errores</span></li>
        <li><span><span class="toc-item-num">12.</span> Conclusión y Competencias del Ingeniero</span></li>
    </ul>
</div>

<!-- ========================================== -->
<!-- MÓDULO 1: FUNDAMENTOS TEÓRICOS -->
<!-- ========================================== -->
<h1>1. Fundamentos Teóricos de Sistemas Distribuidos</h1>

<p>
Para superar con la máxima calificación este laboratorio en 3º de Grado en Ingeniería Informática, es crucial comprender el fundamento conceptual detrás de cada línea de código. Un sistema distribuido se caracteriza por componerse de múltiples nodos independientes que se coordinan mediante paso de mensajes.
</p>

<h2>1.1 ¿Qué es una Llamada a Procedimiento Remoto (RPC)?</h2>
<p>
En un sistema centralizado clásico, una función se invoca mediante una <em>llamada a procedimiento local</em> (LPC), donde los argumentos se sitúan en la pila del hilo y la CPU salta a una dirección del mismo espacio virtual de memoria.
</p>
<p>
En un <strong>Sistema Distribuido</strong>, los procesos residen en espacios de memoria completamente aislados. El paradigma de <strong>RPC (Remote Procedure Call)</strong> busca ofrecer <strong>transparencia de localización</strong>: que la invocación a una función ejecutada en otra máquina o proceso se escriba y se perciba idéntica a una función local de C#.
</p>

{callout("why", "El Principio de Transparencia de Red y sus Límites", 
"""Aunque RPC persigue la <em>transparencia sintáctica</em>, la teoría clásica (Falacias de la Computación Distribuida de Deutsch) demuestra que <strong>nunca existe transparencia semántica absoluta</strong>:<br>
• Una llamada local nunca falla por caída del cable de red o congestión de routers.<br>
• Una llamada RPC puede experimentar latencia indeterminada, fallos parciales o caídas del servidor remoto.<br>
Por ello, gRPC fuerza el uso de tipos asíncronos (<code class='inline'>Task</code>), cancelaciones y el control explícito de excepciones remotas con <code class='inline'>RpcException</code>.""")}

<h2>1.2 Anatomía de una Llamada RPC: Stubs y Skeletons</h2>
<p>
Para ocultar la complejidad de los sockets TCP y la codificación de tramas binarias, el middleware genera automáticamente dos componentes fundamentales:
</p>
<ul>
    <li><strong>Stub (Lado Cliente):</strong> Actúa como proxy o representante local del servicio remoto. Empaqueta los argumentos en un búfer binario estructurado (<strong>Marshalling</strong> o Serialización) y despacha la trama por la red.</li>
    <li><strong>Skeleton / Base Service (Lado Servidor):</strong> Recibe el mensaje binario, extrae los objetos originales de C# (<strong>Unmarshalling</strong> o Deserialización), despacha la ejecución al método real en <code class="inline">RestauranteService</code> y empaqueta el resultado de retorno.</li>
</ul>

<!-- DIAGRAMA STUB SKELETON CON FLECHAS SVG DEFINIDAS -->
<div class="diagram-container avoid-break">
    <svg width="600" height="135" viewBox="0 0 600 135" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
            </marker>
        </defs>
        <!-- Cliente -->
        <rect x="10" y="15" width="120" height="95" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
        <text x="70" y="40" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#1e3a8a">CLIENTE (App)</text>
        <text x="70" y="65" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#1e40af">Invoca método</text>
        <text x="70" y="80" font-family="monospace" font-size="8" text-anchor="middle" fill="#0f172a">HacerPedido()</text>

        <!-- Stub -->
        <rect x="150" y="15" width="115" height="95" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
        <text x="207" y="40" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#92400e">CLIENT STUB</text>
        <text x="207" y="65" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#78350f">1. Marshalling</text>
        <text x="207" y="82" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#78350f">2. Envío HTTP/2</text>

        <!-- Canal Red -->
        <path d="M 265 62 L 325 62" stroke="#059669" stroke-width="3" stroke-dasharray="4" marker-end="url(#arrow)"/>
        <text x="295" y="52" font-family="sans-serif" font-size="7.5" font-weight="bold" text-anchor="middle" fill="#065f46">RED (HTTP/2)</text>
        <text x="295" y="78" font-family="sans-serif" font-size="7" text-anchor="middle" fill="#047857">Trama Binaria</text>

        <!-- Skeleton -->
        <rect x="330" y="15" width="120" height="95" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
        <text x="390" y="40" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#92400e">SKELETON (Base)</text>
        <text x="390" y="65" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#78350f">3. Unmarshalling</text>
        <text x="390" y="82" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#78350f">4. Despacho método</text>

        <!-- Servidor -->
        <rect x="470" y="15" width="120" height="95" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
        <text x="530" y="40" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#14532d">SERVIDOR (Lógica)</text>
        <text x="530" y="65" font-family="sans-serif" font-size="8.5" text-anchor="middle" fill="#166534">Ejecuta servicio</text>
        <text x="530" y="80" font-family="monospace" font-size="8" text-anchor="middle" fill="#0f172a">RestauranteService</text>
    </svg>
    <div class="diagram-caption">Figura 1.1: Flujo de invocación remota RPC mediante Stubs (Cliente) y Skeletons (Servidor).</div>
</div>

<h2>1.3 ¿Por qué gRPC y Protocol Buffers en vez de REST y JSON?</h2>
<p>
Mientras que las arquitecturas web tradicionales emplean REST sobre HTTP/1.1 con texto JSON, las arquitecturas de microservicios distribuidos de alta concurrencia prefieren gRPC por motivos de eficiencia crítica:
</p>

<table>
    <thead>
        <tr>
            <th>Dimensión Técnica</th>
            <th>Arquitectura REST con JSON</th>
            <th>gRPC con Protocol Buffers</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Formato del Mensaje</strong></td>
            <td>Texto plano estructurado (UTF-8). Ineficiente en tamaño y CPU.</td>
            <td><strong>Binario compacto</strong> mediante Varints y Tags de campo.</td>
        </tr>
        <tr>
            <td><strong>Contrato Formal</strong></td>
            <td>Opcional o tardío (OpenAPI/Swagger). Sujeto a desincronizaciones en runtime.</td>
            <td><strong>Estricto y obligatorio</strong> vía IDL (<code class="inline">.proto</code>). Comprobado en compilación.</td>
        </tr>
        <tr>
            <td><strong>Transporte de Red</strong></td>
            <td>HTTP/1.1 (o HTTP/2 no optimizado). Múltiples conexiones TCP.</td>
            <td><strong>HTTP/2 puro</strong> con multiplexación sobre un único socket TCP permanente.</td>
        </tr>
        <tr>
            <td><strong>Carga de CPU</strong></td>
            <td>Alta: El procesador parsea cadenas, comillas, llaves y convierte números a texto.</td>
            <td><strong>Mínima:</strong> Deserialización directa mediante desplazamientos binarios en RAM.</td>
        </tr>
        <tr>
            <td><strong>Streaming</strong></td>
            <td>Complejo (requiere WebSockets o SSE).</td>
            <td><strong>Nativo de 4 tipos:</strong> Unario, Client Streaming, Server Streaming y Bidireccional.</td>
        </tr>
    </tbody>
</table>

{callout("example", "Ejemplo Visual: Comparativa de Sobrecarga de Red (Payload Overhead)", 
"""Para enviar un pedido con <code class='inline'>id_pedido = 1</code> y <code class='inline'>distancia = 5</code>:<br>
• <strong>En JSON (REST):</strong> <code class='inline'>{"id_pedido":1,"distancia":5}</code> ocupa <strong>32 bytes</strong> en texto ASCII.<br>
• <strong>En Protobuf:</strong> Se codifica en solo <strong>4 bytes</strong> hexadecimales: <code class='inline'>08 01 10 05</code> (Tag 1 = 1, Tag 2 = 5).<br>
<strong>Resultado:</strong> ¡Un <strong>87.5% de ahorro en ancho de banda</strong> en cada llamada!""")}

<h2>1.4 Concurrencia en un Servidor con Estado (Stateful)</h2>
<p>
En un servidor gRPC con estado en memoria, varios hilos atienden peticiones simultáneamente. Esto genera dos riesgos críticos:
</p>
<ol>
    <li><strong>Condición de Carrera en Operaciones Compuestas (Check-Then-Act):</strong> Si dos clientes hacen un pedido cuando la cola tiene 9 de 10 elementos, ambos hilos podrían comprobar la condición <code class="inline">Count &lt; 10</code> a la vez y encolar simultáneamente, superando la capacidad máxima de 10 pedidos.</li>
    <li><strong>Desperdicio de Hilos por Espera Activa:</strong> Si el repartidor consultara la cola en un bucle continuo de sondeo (polling), saturaría la CPU de la máquina.</li>
</ol>

{callout("exam", "Pregunta de Examen: ¿Por qué no usar 'Thread.Sleep' o un bucle 'while'?", 
"""Un bucle <code class='inline'>while (cola.IsEmpty) {{ Thread.Sleep(100); }}</code> retiene un hilo del pool de ASP.NET Core bloqueado inútilmente.<br>
En su lugar, utilizamos un <strong>semáforo asíncrono (<code class='inline'>SemaphoreSlim</code>)</strong>: el hilo del repartidor se libera mediante <code class='inline'>await _readyOrdersSemaphore.WaitAsync()</code>, y Kestrel puede reutilizar ese hilo de CPU para atender a otros clientes. Cuando entra un pedido, <code class='inline'>Release()</code> despierta al repartidor de manera reactiva e instantánea.""")}

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 2: ARQUITECTURA GLOBAL DEL SISTEMA -->
<!-- ========================================== -->
<h1>2. Arquitectura Global del Sistema</h1>

<p>
El sistema distribuido está estructurado en tres procesos independientes que se comunican en tiempo real mediante el puerto TCP 5000:
</p>

<!-- DIAGRAMA ARQUITECTURA GLOBAL CON FLECHAS -->
<div class="diagram-container avoid-break">
    <svg width="650" height="250" viewBox="0 0 650 250" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
            </marker>
            <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
            </marker>
            <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/>
            </marker>
        </defs>

        <!-- NODO CLIENTE -->
        <g>
            <rect x="20" y="15" width="165" height="215" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
            <rect x="20" y="15" width="165" height="32" rx="8" fill="#3b82f6"/>
            <text x="102" y="36" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#ffffff">NODO CLIENTE</text>
            <text x="102" y="62" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#1e3a8a">Terminal 3 (Proceso CLI)</text>
            
            <rect x="30" y="75" width="145" height="36" rx="5" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="102" y="91" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#0369a1">Interfaz CLI (Menú)</text>
            <text x="102" y="103" font-family="sans-serif" font-size="7" text-anchor="middle" fill="#0284c7">Opciones: 1, 2, 3</text>

            <rect x="30" y="120" width="145" height="42" rx="5" fill="#e0f2fe" stroke="#0284c7"/>
            <text x="102" y="136" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#0369a1">RestauranteClienteService</text>
            <text x="102" y="148" font-family="sans-serif" font-size="7" text-anchor="middle" fill="#0284c7">GrpcChannel (localhost:5000)</text>
            <text x="102" y="158" font-family="sans-serif" font-size="6.5" text-anchor="middle" fill="#0369a1">Switch: Http2Unencrypted</text>

            <text x="102" y="195" font-family="sans-serif" font-size="8" font-style="italic" text-anchor="middle" fill="#64748b">Rol: PRODUCTOR</text>
        </g>

        <!-- NODO SERVIDOR (RESTAURANTE) -->
        <g>
            <rect x="235" y="15" width="185" height="215" rx="8" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
            <rect x="235" y="15" width="185" height="32" rx="8" fill="#10b981"/>
            <text x="327" y="36" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#ffffff">NODO RESTAURANTE</text>
            <text x="327" y="62" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#065f46">Servidor gRPC Kestrel :5000</text>

            <!-- Estructuras de memoria -->
            <rect x="245" y="75" width="165" height="28" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text x="327" y="93" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" fill="#14532d">_ordersQueue (Max: 10)</text>

            <rect x="245" y="108" width="165" height="28" rx="4" fill="#dcfce7" stroke="#16a34a"/>
            <text x="327" y="126" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" fill="#14532d">_allOrders (Historial)</text>

            <rect x="245" y="141" width="165" height="28" rx="4" fill="#fef3c7" stroke="#d97706"/>
            <text x="327" y="159" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" fill="#92400e">_readyOrdersSemaphore</text>

            <rect x="245" y="174" width="165" height="24" rx="4" fill="#fee2e2" stroke="#dc2626"/>
            <text x="327" y="190" font-family="monospace" font-size="7.5" font-weight="bold" text-anchor="middle" fill="#991b1b">lock (_takeLock)</text>

            <text x="327" y="218" font-family="sans-serif" font-size="7.5" font-style="italic" text-anchor="middle" fill="#64748b">Servicio Singleton en Memoria</text>
        </g>

        <!-- NODO REPARTIDOR -->
        <g>
            <rect x="470" y="15" width="160" height="215" rx="8" fill="#f8fafc" stroke="#f59e0b" stroke-width="2"/>
            <rect x="470" y="15" width="160" height="32" rx="8" fill="#f59e0b"/>
            <text x="550" y="36" font-family="sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle" fill="#ffffff">NODO REPARTIDOR</text>
            <text x="550" y="62" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#92400e">Terminal 2 (Worker Daemon)</text>

            <rect x="480" y="75" width="140" height="36" rx="5" fill="#fef3c7" stroke="#d97706"/>
            <text x="550" y="91" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#92400e">Worker Loop</text>
            <text x="550" y="103" font-family="monospace" font-size="7" text-anchor="middle" fill="#b45309">while (true)</text>

            <rect x="480" y="120" width="140" height="38" rx="5" fill="#fef3c7" stroke="#d97706"/>
            <text x="550" y="136" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle" fill="#92400e">Simulador de Entrega</text>
            <text x="550" y="148" font-family="monospace" font-size="7" text-anchor="middle" fill="#b45309">Task.Delay(3000)</text>

            <text x="550" y="195" font-family="sans-serif" font-size="8" font-style="italic" text-anchor="middle" fill="#64748b">Rol: CONSUMIDOR</text>
        </g>

        <!-- FLECHAS DE COMUNICACIÓN -->
        <path d="M 185 90 L 235 90" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
        <text x="210" y="84" font-family="sans-serif" font-size="6.8" font-weight="bold" text-anchor="middle" fill="#1e40af">HacerPedido</text>

        <path d="M 185 130 L 235 130" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
        <text x="210" y="124" font-family="sans-serif" font-size="6.8" font-weight="bold" text-anchor="middle" fill="#1e40af">Consultar</text>

        <path d="M 470 95 L 420 95" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-amber)"/>
        <text x="445" y="89" font-family="sans-serif" font-size="6.5" font-weight="bold" text-anchor="middle" fill="#92400e">TomarPedido</text>

        <path d="M 420 115 L 470 115" stroke="#10b981" stroke-width="2" marker-end="url(#arrow-green)"/>
        <text x="445" y="127" font-family="sans-serif" font-size="6.5" font-weight="bold" text-anchor="middle" fill="#047857">Asignación</text>
    </svg>
    <div class="diagram-caption">Figura 2.1: Arquitectura física de los tres procesos y canales de comunicación gRPC sobre HTTP/2.</div>
</div>

<h2>2.1 El Patrón Productor-Consumidor con Búfer Acotado</h2>
<p>
El flujo algorítmico sigue las reglas canónicas de la computación concurrente:
</p>
<ol>
    <li><strong>El Productor (Cliente):</strong> Genera solicitudes mediante <code class="inline">HacerPedido</code>. Verifica que la cola no exceda la capacidad máxima (<code class="inline">MaxQueueCapacity = 10</code>). Si la cola está llena, el servidor rechaza la comanda devolviendo un error gRPC <code class="inline">StatusCode.ResourceExhausted</code>.</li>
    <li><strong>El Búfer (Restaurante):</strong> Mantiene la cola compartida <code class="inline">ConcurrentQueue&lt;Pedido&gt;</code> y un semáforo contador (<code class="inline">SemaphoreSlim</code>) inicializado a 0 permisos.</li>
    <li><strong>El Consumidor (Repartidor):</strong> Solicita pedidos llamando a <code class="inline">TomarPedidoParaRepartir</code>. Si no hay pedidos, queda a la espera en el semáforo. Cuando un cliente encola un pedido, ejecuta <code class="inline">_readyOrdersSemaphore.Release()</code>, despertando inmediatamente al repartidor.</li>
</ol>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 3: CONSTRUCCIÓN DESDE CERO -->
<!-- ========================================== -->
<h1>3. Construcción del Proyecto Desde Cero con el CLI de .NET</h1>

<p>
Para levantar este proyecto desde un terminal en blanco (por ejemplo, en el examen de laboratorio), ejecuta los siguientes comandos exactos:
</p>

<h2>3.1 Paso 1: Creación de la Solución y los Proyectos</h2>
{code_block_html("Comandos CLI de Inicialización", "Terminal / Consola", "bash", """# 1. Crear la carpeta raíz y acceder a ella
mkdir SistemaRestaurante
cd SistemaRestaurante

# 2. Crear la solución de .NET
dotnet new sln -n SistemaRestaurante

# 3. Crear el proyecto Web/Kestrel para el Servidor
dotnet new web -n Restaurante

# 4. Crear los dos proyectos de Consola para los clientes
dotnet new console -n Repartidor
dotnet new console -n Cliente

# 5. Agregar los tres proyectos a la solución
dotnet sln add Restaurante/Restaurante.csproj
dotnet sln add Repartidor/Repartidor.csproj
dotnet sln add Cliente/Cliente.csproj

# 6. Crear el directorio compartido para los contratos Protocol Buffers
mkdir Protos
""")}

<h2>3.2 Paso 2: Instalación de Dependencias NuGet de gRPC</h2>
{code_block_html("Comandos CLI para Instalar Paquetes NuGet", "Terminal / Consola", "bash", """# 1. Paquete del Servidor (incluye Kestrel HTTP/2 y generador de server stubs):
dotnet add Restaurante package Grpc.AspNetCore

# 2. Paquetes del Repartidor (cliente HTTP/2, Protobuf runtime y compilador protoc):
dotnet add Repartidor package Grpc.Net.Client
dotnet add Repartidor package Google.Protobuf
dotnet add Repartidor package Grpc.Tools

# 3. Paquetes del Cliente:
dotnet add Cliente package Grpc.Net.Client
dotnet add Cliente package Google.Protobuf
dotnet add Cliente package Grpc.Tools
""")}

{callout("step", "Estructura de Directorios Resultante", 
"""Verifica que la estructura de carpetas en tu workspace coincida con el siguiente esquema:<br>
<pre style='margin: 4px 0; font-family: monospace; font-size: 7.8pt;'>
SistemaRestaurante/
├── SistemaRestaurante.slnx (o .sln)
├── Protos/
│   └── restaurante.proto
├── Restaurante/
│   ├── Restaurante.csproj
│   ├── Program.cs
│   ├── Pedido.cs
│   └── RestauranteService.cs
├── Repartidor/
│   ├── Repartidor.csproj
│   └── Program.cs
└── Cliente/
    ├── Cliente.csproj
    ├── Program.cs
    └── RestauranteClienteService.cs
</pre>""")}

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 4: EL CONTRATO DE COMUNICACIÓN -->
<!-- ========================================== -->
<h1>4. El Contrato de Comunicación: Protos/restaurante.proto</h1>

<p>
El archivo <code class="inline">.proto</code> constituye la <strong>Única Fuente de Verdad (Single Source of Truth)</strong> del sistema distribuido.
</p>

{code_block_html("Definición de Servicios y Mensajes Protobuf", "Protos/restaurante.proto", "proto", proto_code)}

<h2>4.1 Desglose Exhaustivo Línea a Línea del Contrato</h2>

<ul>
    <li><code class="inline">syntax = "proto3";</code> (Línea 1): Define la versión 3 de la sintaxis de Protocol Buffers. En <code class="inline">proto3</code> todos los campos son opcionales por defecto y no existe <code class="inline">required</code>, garantizando compatibilidad evolutiva sin roturas.</li>
    <li><code class="inline">option csharp_namespace = "Restaurante";</code> (Línea 2): Especifica el espacio de nombres de C# en el que se ubicarán las clases generadas automáticamente.</li>
    <li><code class="inline">import "google/protobuf/empty.proto";</code> (Línea 3): En gRPC, todo método RPC debe recibir obligatoriamente un mensaje y devolver otro. Google provee el tipo estándar <code class="inline">google.protobuf.Empty</code> para aquellos métodos sin argumentos de entrada.</li>
    <li><strong>Definición del Servicio <code class="inline">RestauranteService</code> (Líneas 5-10):</strong> Declara 4 procedimientos remotos unarios:
        <ol>
            <li><code class="inline">HacerPedido (PedidoRequest) returns (PedidoResponse);</code>: El cliente envía la comanda con platos y distancia, y recibe el identificador del pedido.</li>
            <li><code class="inline">ConsultarEstadoPedido (ConsultaRequest) returns (EstadoResponse);</code>: Permite consultar en qué fase se encuentra un pedido dado su ID.</li>
            <li><code class="inline">TomarPedidoParaRepartir (google.protobuf.Empty) returns (PedidoResponse);</code>: Invocado por el repartidor para extraer el siguiente pedido listo.</li>
            <li><code class="inline">ConsultarPlatosPedido (ConsultaRequest) returns (PedidoResponse);</code>: Devuelve la lista detallada de platos asociados a un pedido.</li>
        </ol>
    </li>
    <li><strong>Colecciones con <code class="inline">repeated</code> (Línea 13):</strong> La directiva <code class="inline">repeated PlatoPedido platos = 1;</code> genera en C# una colección de tipo <code class="inline">Google.Protobuf.Collections.RepeatedField&lt;PlatoPedido&gt;</code>.</li>
    <li><strong>Los Números de Campo (<code class="inline">= 1, = 2</code>):</strong> 
        {callout("exam", "Pregunta de Examen: ¿Qué significan los números '= 1' y '= 2' en los campos Protobuf?", 
        """¡NO son valores por defecto! Son <strong>etiquetas de campo binarias (Field Tags)</strong>. En la trama binaria de la red, gRPC no transmite cadenas de texto como 'distancia', sino el tag numérico <code class='inline'>2</code> en 1 byte. Por esta razón, <strong>nunca se debe modificar el número de un campo en un sistema desplegado</strong>, pues rompería la compatibilidad binaria.""")}
    </li>
</ul>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 5: CONFIGURACIÓN DE LOS .CSPROJ -->
<!-- ========================================== -->
<h1>5. Configuración de los Proyectos (.csproj)</h1>

<p>
La compilación de archivos Protobuf se gestiona mediante tareas de MSBuild integradas por el paquete <code class="inline">Grpc.Tools</code>.
</p>

<h2>5.1 Configuración del Servidor: Restaurante.csproj</h2>
{code_block_html("Proyecto del Servidor gRPC", "Restaurante/Restaurante.csproj", "xml", rest_proj)}

<h2>5.2 Configuración del Repartidor: Repartidor.csproj</h2>
{code_block_html("Proyecto del Repartidor (Worker Client)", "Repartidor/Repartidor.csproj", "xml", rep_proj)}

<h2>5.3 Configuración del Cliente: Cliente.csproj</h2>
{code_block_html("Proyecto del Cliente Interactivo", "Cliente/Cliente.csproj", "xml", cli_proj)}

{callout("why", "El Porqué Técnico de 'GrpcServices=Server' frente a 'GrpcServices=Client'", 
"""Al compilar con <code class='inline'>dotnet build</code>, el compilador <code class='inline'>protoc</code> analiza el atributo <code class='inline'>GrpcServices</code>:<br>
• <code class='inline'>GrpcServices="Server"</code>: Genera la clase abstracta <code class='inline'>RestauranteServiceBase</code>, que contiene los métodos virtuales que el servidor debe sobreescribir (<code class='inline'>override</code>).<br>
• <code class='inline'>GrpcServices="Client"</code>: Genera la clase concreta <code class='inline'>RestauranteServiceClient</code> (el Stub), que implementa los métodos de red (<code class='inline'>HacerPedidoAsync</code>, etc.).<br>
Si olvidáramos esta directiva, las clases correspondientes no se generarían y el código no compilaría.""")}

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 6: EL SERVIDOR (RESTAURANTE) -->
<!-- ========================================== -->
<h1>6. Implementación del Servidor (Restaurante)</h1>

<p>
El servidor coordina todo el ciclo de vida de los pedidos, implementando el modelo de dominio, la configuración de Kestrel y la sincronización concurrente.
</p>

<h2>6.1 El Modelo de Dominio Interno: Restaurante/Pedido.cs</h2>
{code_block_html("Clase Entidad de Pedido Interno", "Restaurante/Pedido.cs", "csharp", rest_pedido)}

<h2>6.2 Punto de Entrada y Configuración de Kestrel: Restaurante/Program.cs</h2>
{code_block_html("Configuración del Host Kestrel y Servicios", "Restaurante/Program.cs", "csharp", rest_prog)}

<h3>Análisis de la Configuración de Kestrel y Dependencias</h3>
<ul>
    <li>
        <strong>HTTP/2 sin TLS (Líneas 10-15):</strong> 
        Por defecto, gRPC requiere HTTP/2 mediante negociación ALPN sobre TLS. En desarrollo local sin certificados, configuramos Kestrel para escuchar en <strong>HTTP/2 en texto claro (h2c)</strong> en el puerto 5000:
        <code class="inline">options.ListenLocalhost(5000, o =&gt; o.Protocols = HttpProtocols.Http2);</code>.
    </li>
    <li>
        <strong>El Singleton Esencial (Línea 21):</strong> 
        <code class="inline">builder.Services.AddSingleton&lt;RestauranteService&gt;();</code>
        {callout("exam", "Pregunta de Examen Clave: ¿Por qué Registrar RestauranteService como Singleton?", 
        """Por defecto, ASP.NET Core registra los servicios gRPC como <strong>Transient</strong> (se crea una instancia nueva por cada petición RPC y se destruye al terminar).<br>
        Si <code class='inline'>RestauranteService</code> fuera Transient, cada llamada a <code class='inline'>HacerPedido</code> o <code class='inline'>TomarPedidoParaRepartir</code> crearía una cola y un diccionario completamente vacíos. ¡Los pedidos se perderían de inmediato!<br>
        Al registrarlo como <strong>Singleton</strong>, el contenedor de dependencias garantiza que existe una <strong>única instancia en memoria</strong> compartida por todos los clientes y repartidores durante toda la ejecución del servidor.""")}
    </li>
    <li>
        <strong>Mapeo del Servicio (Línea 26):</strong> 
        <code class="inline">app.MapGrpcService&lt;RestauranteService&gt;();</code> enruta el tráfico HTTP/2 gRPC entrante hacia los métodos de nuestra clase.
    </li>
</ul>

<div class="page-break"></div>

<h2>6.3 La Lógica de Negocio y Concurrencia: Restaurante/RestauranteService.cs</h2>
<p>
A continuación se presenta el código completo del servicio gRPC del servidor:
</p>
{code_block_html("Servicio gRPC con Manejo de Concurrencia", "Restaurante/RestauranteService.cs", "csharp", rest_service, allow_break=True)}

<div class="page-break"></div>

<h3>Desglose Exhaustivo de Concurrencia en RestauranteService</h3>

<h3>1. Estructuras de Datos y Sincronización (Líneas 15-22):</h3>
<ul>
    <li><code class="inline">ConcurrentQueue&lt;Pedido&gt; _ordersQueue;</code>: Cola FIFO thread-safe que almacena los pedidos listos para ser recogidos por el repartidor.</li>
    <li><code class="inline">ConcurrentDictionary&lt;int, Pedido&gt; _allOrders;</code>: 
        {callout("why", "El Porqué del Diccionario Histórico ConcurrentDictionary", 
        """Cuando el repartidor invoca <code class='inline'>TomarPedidoParaRepartir</code>, el pedido se <strong>desencola</strong> (se elimina de <code class='inline'>_ordersQueue</code>). Si un cliente ejecuta posteriormente <code class='inline'>ConsultarEstadoPedido(id)</code> y solo tuviéramos la cola, ¡el sistema diría que el pedido no existe!<br>
        El <code class='inline'>_allOrders</code> actúa como el <strong>registro histórico persistente en memoria</strong>, manteniendo el objeto accesible en tiempo constante O(1) para consultar su estado ('En reparto') en todo momento.""")}
    </li>
    <li><code class="inline">SemaphoreSlim _readyOrdersSemaphore = new SemaphoreSlim(0);</code>: 
        Semáforo contador inicializado a <strong>0 permisos</strong>. Cuando no hay pedidos, cualquier repartidor que invoque <code class="inline">WaitAsync()</code> queda pausado asíncronamente. Al entrar un pedido, <code class="inline">Release()</code> suma un permiso y lo desbloquea.
    </li>
    <li><code class="inline">object _takeLock = new object();</code>: 
        {callout("warning", "¿Por qué hace falta 'lock' si ConcurrentQueue ya es thread-safe?", 
        """Las colecciones concurrentes solo protegen operaciones atómicas aisladas (<code class='inline'>Enqueue</code> o <code class='inline'>TryDequeue</code>).<br>
        Sin embargo, la secuencia:
        <code class='inline'>if (_ordersQueue.Count &lt; MaxQueueCapacity) {{ _ordersQueue.Enqueue(...); }}</code>
        es una operación compuesta (<strong>Check-Then-Act</strong>). Si dos peticiones leen <code class='inline'>Count = 9</code> simultáneamente, ambas pasarán el <code class='inline'>if</code> y la cola terminará con 11 elementos. El cerrojo <code class='inline'>lock (_takeLock)</code> asegura que la comprobación y la inserción se ejecuten de forma atómica indivisible.""")}
    </li>
</ul>

<h3>2. Análisis de los Métodos RPC:</h3>
<ul>
    <li>
        <strong><code class="inline">HacerPedido</code> (Líneas 34-65):</strong>
        Adquiere el cerrojo <code class="inline">lock (_takeLock)</code>, comprueba si <code class="inline">_ordersQueue.Count &lt; MaxQueueCapacity</code>. Si hay espacio, crea el pedido, lo añade a la cola y al diccionario histórico, incrementa el semáforo con <code class="inline">_readyOrdersSemaphore.Release()</code> y responde al cliente. Si la cola está saturada (10 pedidos), lanza una <code class="inline">RpcException(new Status(StatusCode.ResourceExhausted, "La cola está llena"))</code>.
    </li>
    <li>
        <strong><code class="inline">ConsultarEstadoPedido</code> (Líneas 67-84):</strong>
        Busca en <code class="inline">_allOrders</code> mediante <code class="inline">TryGetValue</code>. Si existe, retorna su estado actual y el tiempo estimado (<code class="inline">distancia * 5</code> mins). Si no existe, lanza un error gRPC con <code class="inline">StatusCode.NotFound</code>.
    </li>
    <li>
        <strong><code class="inline">TomarPedidoParaRepartir</code> (Líneas 86-104):</strong>
        Ejecuta <code class="inline">await _readyOrdersSemaphore.WaitAsync();</code>, suspendiéndose asíncronamente si no hay pedidos. Al recibir el permiso, adquiere el cerrojo, realiza <code class="inline">_ordersQueue.TryDequeue</code>, muta el estado a "En reparto" y devuelve los datos al repartidor.
    </li>
    <li>
        <strong><code class="inline">ConsultarPlatosPedido</code> (Líneas 106-120):</strong>
        Recupera el pedido del diccionario y formatea la comanda de platos utilizando <code class="inline">string.Join</code>.
    </li>
</ul>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 7: EL REPARTIDOR -->
<!-- ========================================== -->
<h1>7. El Agente Consumidor (Repartidor)</h1>

<p>
El repartidor es un cliente gRPC que opera como un <strong>Worker de fondo (Daemon)</strong>. Consume pedidos continuamente en un bucle infinito y simula el trayecto físico de entrega.
</p>

{code_block_html("Worker Loop Asíncrono del Repartidor", "Repartidor/Program.cs", "csharp", rep_prog)}

<h2>7.1 Análisis del Funcionamiento del Repartidor</h2>
<ul>
    <li><strong>Creación del Canal (Línea 20):</strong> <code class="inline">GrpcChannel.ForAddress("http://localhost:5000", ...)</code> inicializa la conexión HTTP/2 hacia el restaurante.</li>
    <li><strong>El Bucle Infinito (Línea 25):</strong> Ejecuta un ciclo continuo <code class="inline">while (true)</code> solicitando tareas de despacho.</li>
    <li><strong>Llamada Remota Asíncrona (Línea 29):</strong> Invoca <code class="inline">await client.TomarPedidoParaRepartirAsync(new Empty())</code>. Gracias al semáforo en el servidor, esta llamada se queda en suspensión en el servidor sin consumir CPU hasta que entra un pedido.</li>
    <li><strong>Simulación de Reparto (Línea 33):</strong> <code class="inline">await Task.Delay(3000);</code> suspende la tarea durante 3 segundos para simular el trayecto en moto/bici.</li>
    <li><strong>Tolerancia a Fallos y Reintentos (Líneas 36-45):</strong> Si el servidor no está encendido o sufre una desconexión, captura <code class="inline">RpcException</code> y reintenta tras 2-3 segundos, impidiendo que el proceso muera.</li>
</ul>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 8: EL CLIENTE -->
<!-- ========================================== -->
<h1>8. La Aplicación Cliente (Cliente)</h1>

<p>
La aplicación cliente separa claramente la lógica de comunicación con gRPC de la interacción con el usuario en consola.
</p>

<h2>8.1 Servicio de Comunicación: Cliente/RestauranteClienteService.cs</h2>
{code_block_html("Encapsulamiento del Stub Cliente gRPC", "Cliente/RestauranteClienteService.cs", "csharp", cli_service)}

{callout("warning", "El Switch de Seguridad: Http2UnencryptedSupport", 
"""En la línea 17 encontramos:
<code class='inline'>AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);</code><br>
<strong>¿Por qué es indispensable?</strong> Por defecto, el manejador de sockets de .NET rechaza negociar HTTP/2 sin cifrado TLS (https). Al conectarse a <code class='inline'>http://localhost:5000</code> en texto claro, si este switch no estuviera activado en runtime, .NET lanzaría una excepción inmediata de tipo <code class='inline'>InvalidOperationException: The HTTP/2 unencrypted support switch must be set</code>.""")}

<div class="page-break"></div>

<h2>8.2 Interfaz de Usuario por Consola: Cliente/Program.cs</h2>
{code_block_html("Menú Interactivo de Usuario", "Cliente/Program.cs", "csharp", cli_prog, allow_break=True)}

<h3>Puntos Clave del Flujo de Usuario:</h3>
<ul>
    <li><strong>Validación Robusta (Líneas 28-36):</strong> Si el usuario pulsa una opción inválida, el sistema muestra "Opción no válida" y vuelve a pedir la entrada sin reimprimir todo el menú repetidamente.</li>
    <li><strong>Composición Dinámica de Platos (Líneas 40-52):</strong> Permite añadir platos en bucle hasta que se pulsa Enter en blanco.</li>
    <li><strong>Colección Protobuf (Líneas 24-26 en ClienteService):</strong> La lista nativa <code class="inline">List&lt;PlatoPedido&gt;</code> se integra en el mensaje gRPC con <code class="inline">request.Platos.AddRange(platos)</code>.</li>
</ul>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 9: GUÍA DE EJECUCIÓN Y CASOS DE PRUEBA -->
<!-- ========================================== -->
<h1>9. Guía de Ejecución y Casos de Prueba Límite</h1>

<p>
Para verificar el comportamiento distribuido, debes ejecutar los tres proyectos simultáneamente en <strong>tres ventanas de terminal independientes</strong> desde la carpeta raíz.
</p>

<h2>9.1 Orden Secuencial de Puesta en Marcha</h2>

<div class="callout callout-step avoid-break">
    <div class="callout-title">Paso 1: Iniciar el Servidor (Restaurante)</div>
    <div class="callout-body">
        En la primera terminal, ejecuta:
        <pre style="margin: 4px 0; font-family: monospace; font-size: 8pt;">dotnet run --project Restaurante</pre>
        <strong>Salida esperada:</strong> <code class="inline">Iniciando servidor gRPC del Restaurante...</code>
    </div>
</div>

<div class="callout callout-step avoid-break">
    <div class="callout-title">Paso 2: Iniciar el Repartidor</div>
    <div class="callout-body">
        En la segunda terminal, ejecuta:
        <pre style="margin: 4px 0; font-family: monospace; font-size: 8pt;">dotnet run --project Repartidor</pre>
        <strong>Salida esperada:</strong> <code class="inline">Repartidor iniciado. Esperando pedidos para repartir...</code>
    </div>
</div>

<div class="callout callout-step avoid-break">
    <div class="callout-title">Paso 3: Iniciar el Cliente</div>
    <div class="callout-body">
        En la tercera terminal, ejecuta:
        <pre style="margin: 4px 0; font-family: monospace; font-size: 8pt;">dotnet run --project Cliente</pre>
        <strong>Salida esperada:</strong> <code class="inline">Conectado al servidor gRPC.</code> seguido del menú interactivo.
    </div>
</div>

<h2>9.2 Escenarios de Demostración Práctica</h2>

<h3>Caso 1: Pedido Básico y Despacho Inmediato</h3>
<ol>
    <li>En el <strong>Cliente</strong>, selecciona <code class="inline">1</code>. Introduce el plato: <em>"Hamburguesa Doble"</em>, cantidad: <em>2</em>. Presiona Enter en blanco para terminar. Distancia: <em>4</em>.</li>
    <li><strong>Respuesta en Cliente:</strong> <code class="inline">[Exito] Pedido ID: 1 - Pedido 1 recibido, tiempo estimado: 20 mins</code>.</li>
    <li><strong>Reacción en Servidor:</strong> <code class="inline">info: Recibido un nuevo pedido con ID 1</code>.</li>
    <li><strong>Reacción en Repartidor:</strong>
        <pre style="margin: 2px 0; font-family: monospace; font-size: 7.8pt;">
[Asignado] Pedido en reparto (ID: 1)
Entregando...
(espera 3 segundos)
[Entregado] Pedido ID: 1 entregado con exito.</pre>
    </li>
    <li>En el <strong>Cliente</strong>, durante los 3 segundos de reparto, pulsa opción <code class="inline">2</code> y consulta el ID <code class="inline">1</code>. Verás: <code class="inline">[Estado] En reparto</code>.</li>
</ol>

<h3>Caso 2: Saturación del Búfer Acotado (Cola Llena)</h3>
<p>
Para demostrar que el control de concurrencia y la capacidad máxima funcionan:
</p>
<ol>
    <li>Detén temporalmente el <strong>Repartidor</strong> pulsando <code class="inline">Ctrl + C</code> en su terminal.</li>
    <li>Desde el <strong>Cliente</strong>, realiza 10 pedidos consecutivos (IDs del 2 al 11). Todos se encolarán con éxito.</li>
    <li>Intenta realizar el <strong>pedido número 11</strong>.</li>
    <li><strong>Resultado:</strong> El servidor rechaza la petición y el cliente muestra por pantalla:
        <pre style="margin: 2px 0; font-family: monospace; font-size: 7.8pt; color: #b91c1c;">
[Error] Code: ResourceExhausted, Mensaje: La cola está llena</pre>
    </li>
    <li>Vuelve a iniciar el Repartidor (<code class="inline">dotnet run --project Repartidor</code>). Verás cómo procesa y vacía la cola acumulada uno por uno sin perder ningún pedido.</li>
</ol>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 10: PREGUNTAS TÍPICAS DE EXAMEN -->
<!-- ========================================== -->
<h1>10. Banco de 10 Preguntas Típicas de Examen / Defensa Oral</h1>

<p>
A continuación se recopilan las 10 preguntas conceptuales más habituales con sus respuestas modelo para obtener la máxima calificación:
</p>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P1: ¿Por qué gRPC utiliza HTTP/2 en lugar de HTTP/1.1 y qué ventajas aporta a este sistema?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> HTTP/1.1 sufre de bloqueo de cabeza de línea a nivel de aplicación (cada petición requiere una conexión TCP o esperar al turno anterior). HTTP/2 introduce <strong>multiplexación mediante streams binarios bidireccionales</strong> sobre una única conexión TCP permanente. Esto permite que múltiples llamadas (como consultar estado y hacer pedidos) viajen simultáneamente por el mismo socket sin bloquearse entre sí, además de comprimir cabeceras con HPACK.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P2: ¿Por qué es necesario registrar RestauranteService como Singleton en el contenedor de dependencias?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> En ASP.NET Core, el ciclo de vida por defecto es <em>Scoped</em> o <em>Transient</em> (se instancia una clase por cada llamada y se destruye al finalizar). Nuestro servidor mantiene un <strong>estado en memoria</strong> (la cola de pedidos, el diccionario y el semáforo). Si no fuera Singleton, cada llamada RPC se ejecutaría sobre una instancia vacía, perdiendo el estado y haciendo imposible que el repartidor recoja los pedidos generados por los clientes.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P3: ¿Por qué se utiliza SemaphoreSlim en lugar de un bucle de comprobación periódica (polling) en el repartidor?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Un bucle de polling con <code class="inline">Thread.Sleep</code> incurre en <em>espera activa</em> o introduce latencia artificial innecesaria, además de malgastar CPU y saturar la red con llamadas vacías repetitivas. <code class="inline">SemaphoreSlim.WaitAsync()</code> proporciona un mecanismo de sincronización <strong>reactivo y no bloqueante</strong>: el hilo del repartidor cede el control al sistema operativo y solo es reactivado cuando el cliente produce un pedido mediante <code class="inline">Release()</code>.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P4: Si ConcurrentQueue ya es una estructura thread-safe, ¿por qué es imprescindible el bloque 'lock (_takeLock)'?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Las colecciones concurrentes solo garantizan atomicidad en operaciones individuales aisladas (<code class="inline">Enqueue</code> o <code class="inline">TryDequeue</code>). Sin embargo, verificar la capacidad máxima y luego encolar (<code class="inline">if (_ordersQueue.Count &lt; MaxQueueCapacity) Enqueue()</code>) es una operación compuesta tipo <em>Check-Then-Act</em>. Dos hilos concurrentes podrían leer simultáneamente que hay 9 pedidos e insertar ambos a la vez, superando el límite de 10. El cerrojo <code class="inline">lock</code> asegura que la comprobación y la inserción se ejecuten como una única sección crítica atómica.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P5: ¿Por qué se mantienen simultáneamente una cola (_ordersQueue) y un diccionario (_allOrders)?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Tienen ciclos de vida y propósitos distintos. La cola implementa el búfer de despacho de pedidos pendientes (una vez que el repartidor lo toma, se elimina con <code class="inline">TryDequeue</code>). Si un cliente intentase consultar el estado de su pedido tras ser asignado, no lo encontraría en la cola. El diccionario actúa como el repositorio histórico persistente en memoria con acceso en tiempo constante O(1), permitiendo monitorizar el estado ("En reparto") hasta el final.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P6: ¿Qué función cumple la directiva GrpcServices en los archivos .csproj?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Indica a la herramienta <code class="inline">protoc</code> (a través de <code class="inline">Grpc.Tools</code>) qué clases de C# debe generar. Con <code class="inline">GrpcServices="Server"</code> genera la clase abstracta base con los métodos virtuales que el servidor debe sobreescribir. Con <code class="inline">GrpcServices="Client"</code> genera el Stub cliente con los métodos remotos asíncronos para invocar al servidor.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P7: ¿Por qué se requiere 'AppContext.SetSwitch("...Http2UnencryptedSupport", true)' en el cliente?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Por motivos de seguridad en producción, el cliente HTTP de .NET (<code class="inline">SocketsHttpHandler</code>) no permite por defecto negociar HTTP/2 sin TLS (texto claro / h2c). Dicho conmutador de compatibilidad autoriza explícitamente el uso de HTTP/2 en texto claro en local (<code class="inline">http://localhost:5000</code>).
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P8: ¿Cómo gestiona gRPC los errores frente a una API REST tradicional?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Mientras que REST utiliza códigos de estado HTTP genéricos (400, 404, 500) y formatos de cuerpo arbitrarios, gRPC utiliza una especificación formal de 16 códigos de estado canónicos (<code class="inline">StatusCode</code>), tales como <code class="inline">NotFound</code>, <code class="inline">ResourceExhausted</code>, <code class="inline">Unavailable</code>, transmitidos mediante cabeceras HTTP/2 en los trailers (<code class="inline">grpc-status</code> y <code class="inline">grpc-message</code>), lanzando una <code class="inline">RpcException</code> fuertemente tipada en el cliente.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P9: ¿Qué semántica de comunicación RPC presenta este sistema?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> gRPC por defecto ofrece una semántica <strong>At-Most-Once (A lo sumo una vez)</strong>: ante un fallo de red o timeout, la llamada no se reintenta automáticamente para evitar duplicar operaciones no idempotentes (como crear dos pedidos idénticos con doble cobro). Para lograr <em>At-Least-Once</em> el cliente debe implementar reintentos explícitos, y para <em>Exactly-Once</em> se necesitarían tokens de idempotencia en el servidor.
    </div>
</div>

<div class="callout callout-exam avoid-break">
    <div class="callout-title">P10: ¿Qué tipos de streaming existen en gRPC y cómo se podría aplicar en esta práctica?</div>
    <div class="callout-body">
        <strong>Respuesta:</strong> Existen 4 tipos: Unario (usado aquí), Server Streaming, Client Streaming y Bidireccional. En esta práctica, el método <code class="inline">ConsultarEstadoPedido</code> podría transformarse en un <strong>Server Streaming RPC</strong>: el cliente solicita el seguimiento de su pedido una sola vez, y el servidor mantiene el canal abierto enviando actualizaciones en tiempo real ("En preparación" -> "En reparto" -> "Entregado") a medida que ocurren los eventos, eliminando la necesidad de consultas periódicas manuales.
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- MÓDULO 11: GUÍA DE RESOLUCIÓN DE PROBLEMAS -->
<!-- ========================================== -->
<h1>11. Chuleta de Depuración y Resolución de Errores</h1>

<p>
Durante el desarrollo y ejecución del laboratorio, es común encontrarse con ciertos errores típicos de configuración en entornos Windows y .NET:
</p>

<table>
    <thead>
        <tr>
            <th>Mensaje de Error / Síntoma</th>
            <th>Causa Raíz</th>
            <th>Solución Inmediata</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code class="inline">Failed to bind to address http://localhost:5000: address already in use</code></td>
            <td>Un proceso anterior del Restaurante quedó ejecutándose en segundo plano ocupando el puerto TCP 5000.</td>
            <td>
                En PowerShell, mata el proceso ejecutando:<br>
                <code class="inline">Stop-Process -Name "Restaurante" -Force</code><br>
                o busca el PID con: <code class="inline">Get-NetTCPConnection -LocalPort 5000</code>.
            </td>
        </tr>
        <tr>
            <td><code class="inline">The HTTP/2 unencrypted support switch must be set</code></td>
            <td>El cliente intenta conectar a <code class="inline">http://</code> (sin TLS) sin autorizar HTTP/2 en texto claro.</td>
            <td>Añade antes de abrir el canal:<br><code class="inline">AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);</code></td>
        </tr>
        <tr>
            <td><code class="inline">Status(StatusCode="Unavailable", Detail="Failed to connect to all addresses")</code></td>
            <td>El cliente o repartidor intentó comunicarse pero el servidor no está en ejecución o el puerto es erróneo.</td>
            <td>Asegúrate de haber iniciado primero la terminal del servidor con <code class="inline">dotnet run --project Restaurante</code> y que esté escuchando en el puerto 5000.</td>
        </tr>
        <tr>
            <td><code class="inline">The type or namespace name 'RestauranteServiceBase' could not be found</code></td>
            <td>Falta compilar el archivo Protobuf o la directiva <code class="inline">GrpcServices="Server"</code> no está en el <code class="inline">.csproj</code>.</td>
            <td>Verifica que <code class="inline">Restaurante.csproj</code> contenga <code class="inline">&lt;Protobuf Include="..\Protos\restaurante.proto" GrpcServices="Server" /&gt;</code> y ejecuta <code class="inline">dotnet build</code>.</td>
        </tr>
    </tbody>
</table>

<!-- ========================================== -->
<!-- MÓDULO 12: CONCLUSIÓN -->
<!-- ========================================== -->
<h2>12. Resumen de Competencias del Ingeniero Informático</h2>
<p>
Al completar este laboratorio, habrás interiorizado los conceptos clave exigidos en la ingeniería de software distribuida moderna:
</p>
<ul>
    <li>Diseño de interfaces formales e interoperables mediante <strong>Protocol Buffers IDL</strong>.</li>
    <li>Manejo de protocolos de transporte binarios y de alto rendimiento sobre <strong>HTTP/2 (h2c)</strong>.</li>
    <li>Control estricto de concurrencia multihilo con <strong>secciones críticas atómicas, búferes acotados y semáforos asíncronos</strong>.</li>
    <li>Gestión del ciclo de vida de componentes distribuidos mediante <strong>Inyección de Dependencias (Singleton)</strong> en .NET 10.</li>
    <li>Manejo canónico de excepciones remotas con <strong>códigos de estado gRPC</strong>.</li>
</ul>

<div style="margin-top: 35px; text-align: center; border-top: 1px solid #cbd5e1; padding-top: 15px; font-size: 8.5pt; color: #64748b;">
    <strong>Laboratorio de Sistemas Distribuidos · Práctica 2</strong> · Diseñado con rigor académico para el Grado en Ingeniería Informática.
</div>

</body>
</html>
"""

html_path = os.path.join(BASE_DIR, "manual_guia_sistemas_distribuidos.html")
pdf_path = os.path.join(BASE_DIR, "Guia_Completa_Practica_Sistemas_Distribuidos.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado con éxito en: {html_path}")

# Compilación a PDF con Microsoft Edge Headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print(f"Compilando PDF usando: {edge_path}...")
cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
    print(f"¡PDF generado con éxito! Archivo: {pdf_path} (Tamaño: {os.path.getsize(pdf_path)} bytes)")
else:
    print(f"Error generando PDF: {res.stderr}")
    sys.exit(1)
