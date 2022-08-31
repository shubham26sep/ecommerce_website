import uvicorn

host = '0.0.0.0'
port = 8000

if __name__ == '__main__':
	uvicorn.run('app.catalog_app:app',
		        host=host,
		        port=port,
		        reload=True,
		        workers=1)
