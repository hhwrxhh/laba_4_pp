from waitress import serve
import laba_4_sol
serve(laba_4_sol.app, host='127.0.0.1', port=5000)
