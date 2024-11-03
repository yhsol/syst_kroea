import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True)  # 개발 시에만 reload=True 