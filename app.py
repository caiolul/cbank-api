# from starlette.applications import Starlette
# from starlette.responses import HTMLResponse
# from starlette.websockets import WebSocket
# from jinja2 import Template
# import uvicorn

# template = """\
# <!DOCTYPE HTML>
# <html>
# <head>
#     <script type = "text/javascript">
#         function runWebsockets() {
#             if ("WebSocket" in window) {
#                 var ws = new WebSocket("ws://localhost:8000/ws");
#                 ws.onopen = function() {
#                     console.log("Sending websocket data");
#                     ws.send("Hello From Client");
#                 };
#                 ws.onmessage = function(e) {
#                     alert(e.data);
#                 };
#                 ws.onclose = function() {
#                     console.log("Closing websocket connection");
#                 };
#             } else {
#                 alert("WS not supported, sorry!");
#             }
#         }
#     </script>
# </head>
# <body><a href="javascript:runWebsockets()">Say Hello From Client</a></body>
# </html>
# """


# app = Starlette()


# @app.route('/')
# async def homepage(request):
#     return HTMLResponse(Template(template).render())


# @app.websocket_route('/ws')
# async def websocket_endpoint(websocket):
#     await websocket.accept()
#     # Process incoming messages
#     while True:
#         mesg = await websocket.receive_text()
#         print(mesg)
#         await websocket.send_text(mesg.replace("Client", "Server"))
#     await websocket.close()


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)


from starlette.applications import Starlette
from starlette.routing import Route
from src.routes.routes import api_routes


app = Starlette(debug=True, routes=api_routes)
