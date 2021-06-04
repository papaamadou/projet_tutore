def get_dependencies(fichier):
    with open(fichier, "r", encoding="utf8") as file:
        lines = file.readlines()
        dependences = []
        indice=[]
        for i,l in enumerate(lines):
            if l[0]=='#' and l[2]=='t':
                indice.append(i-2)

        for i in range(len(indice)-1):
            dependence = "\n".join(lines[indice[i]:indice[i+1]])
            dependences.append(dependence)
    return dependences

    def build_html_page(filename,fichier):
    with open(filename,'w',encoding="utf8") as file:
        header = ' <!DOCTYPE html> <html> <head> <script src="https://unpkg.com/reactive-dep-tree@0.2.0/dist/reactive-dep-tree.umd.js" async deferred></script> <title>Read Text File</title> </head><body>'
        file.write(header)
        dependences = get_dependencies(fichier)
        for dep in dependences:
            file.write('<reactive-dep-tree interactive="true" conll="'+dep+'" ></reactive-dep-tree>')
        file.write("</body>")