def pyclick(e):
    e.preventDefault()
    alert(e)

def mutate(e):
    e.preventDefault()
    e.target.innerHTML = "It Works!"
    def restore():
        e.target.innerHTML = "Try Me, I Dare You..."
    setTimeout(restore, 1000)
