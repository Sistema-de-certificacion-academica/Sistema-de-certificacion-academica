

app = FastAPI(
    title="UniCert API",
    description="Sistema de Certificación Académica Digital",
    version="1.0.0",
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


app.include_router(usuarios_router)


@app.get("/")
def root():
    return {"message": "UniCert API funcionando"}
