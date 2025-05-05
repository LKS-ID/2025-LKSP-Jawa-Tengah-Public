from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML = r'''
<!DOCTYPE html>
<html>
<head>
    <title>Assembly Interpreter</title>
</head>
<body style="font-family: monospace; padding: 20px">
    <h2>Assembly x86-64 Runner</h2>
    <p>paste this and you will get hello world</p>
    <pre><b>// write(1, "hello world", 13)
mov rbx, 0xa646c72
mov rcx, 0x6f77206f6c6c6568
push rbx
push rcx
mov rsi, rsp
mov rax, 1
mov rdi, 1
mov rdx, 13
syscall

// exit(0)
mov rax, 60
xor rdi, rdi
syscall
    </b></pre>
    <form method="POST">
        <textarea name="code" rows="16" cols="60">{{ code }}</textarea><br><br>
        <button type="submit">Run</button>
    </form>
    {% if output %}
    <h3>Output:</h3>
    <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    user_input = ""
    if request.method == "POST":
        user_input = request.form.get("code", "").strip()
        if user_input:
            try:
                from pwnlib.asm import asm
                from pwnlib.context import context
                context.arch = 'amd64'
                context.os = 'linux'
                compiled_code = asm(user_input)
                result = subprocess.check_output(["./main", compiled_code.hex()],stderr=subprocess.STDOUT,timeout=2)
                output = result.decode(errors="replace")
            except subprocess.CalledProcessError as e:
                output = f"Error:\n{e.output.decode(errors='replace')}"
            except subprocess.TimeoutExpired:
                output = "Execution timed out."
            except Exception as e:
                output = f"An error occurred: {str(e)}"
            user_input = ""
    return render_template_string(HTML, output=output, code=user_input)
