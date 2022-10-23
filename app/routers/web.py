from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter
import aiohttp

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

url = "http://localhost:8000"

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/register")
def registration(request: Request):
    msj = ""
    return templates.TemplateResponse("create_user.html", {"request": request, "msj": msj})

@router.post("/register")
async def registration(request: Request):
    form = await request.form()
    usuario = {
        "username": form.get('username'),
        "password": form.get('password'),
        "nombre": form.get('nombre'),
        "apellido": form.get('apellido'),
        "correo": form.get('correo'),
        "direccion": form.get('direccion'),
        "telefono": form.get('telefono')
    }
    print(usuario)
    url_post = f"{url}/user/"
    print(f"{url_post}")
    #r = requests.post(url=url, json=usuario)
    async with aiohttp.ClientSession() as session:
        response = await session.request(method="POST",url=url_post, json=usuario)
        response_json = await response.json()
        print(f"Final: {response_json}")
        if "Response" in response_json:
            msj = "Usuario creado satisfactoriamente"
            type_alert = "primary"
        else:
            msj = "Usuario no creado"
            type_alert = "danger"
        return templates.TemplateResponse("create_user.html", {"request": request, "msj": msj, "type_alert": type_alert})

