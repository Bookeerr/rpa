"""API efimera de demostracion, solo loopback. Nunca accede a MySQL."""
from api.app import create_app, MemoryReceiptStore
from auxiliaries.studio_demo import DEMO_TOKEN

if __name__=='__main__':
    print('DEMO SINTETICA: memoria volatil en 127.0.0.1:18080; Ctrl+C detiene.')
    create_app({'API_TOKEN':DEMO_TOKEN},MemoryReceiptStore()).run(
        host='127.0.0.1',port=18080,debug=False,use_reloader=False)
