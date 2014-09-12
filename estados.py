import sys
estadosMap = {
    'separador':["\n"," ","","\t",'\v','\\'],
    'numeros':{
        'estado':'estado6',
        'val':[str(i) for i in range(1,10)]
    },
    'negacion':{
        'estado':'estado30',
        'val':'!'
    },
    'igual':{
        'estado':'estado20',
        'val':'='
    },
    'porcentaje':{
        'estado':'estado31',
        'val':'%'
    },
    'amperson':{
        'estado':'estado32',
        'val':'&'
    },
    'parabierto':{
        'estado':'estado35',
        'val':'('
    },
    'parcerrado':{
        'estado':'estado38',
        'val':')'
    },
    'asterisco':{
        'estado':'estado36',
        'val':'*'
    },
    'sum':{
        'estado':'estado40',
        'val':'+'
    },
    'coma':{
        'estado':'estado42',
        'val':','
    },
    'res':{
        'estado':'estado43',
        'val':'-'
    },
    'mayor':{
        'estado':'estado22',
        'val':'>'
    },
    'menor':{
        'estado':'estado51',
        'val':'<'
    },
    'puntoComa':{
        'estado':'estado47',
        'val':';'
    },
    'slash':{
        'estado':'estado48',
        'val':'/'
    },
    'dospuntos':{
        'estado':'estado50',
        'val': ':'
    },
    'llaveabierto':{
        'estado':'estado58',
        'val':'{'
    },
    'pipe':{
        'estado':'estado59',
        'val':'|'
    },
    'llavecerrado':{
        'estado':'estado62',
        'val':'}'
    },  
    'letras':{
        'estado':'estado13',
        'val':[chr(i) for i in range(97,123)] +[chr(i) for i in range(65,91)]
    },
    'e':['e','E'],
    'hex':['x','X'],
    'af':[chr(i) for i in range(97,103)]+[chr(i) for i in range(65,71)],
    'oct':[str(i) for i in range(8)],
    'pregunta':{
        'estado':'estado26',
        'val':'?'
    },
    'corcheteabierto':{
        'estado':'estado27',
        'val':'['
    },
    'corchetecerrado':{
        'estado':'estado28',
        'val':']'
    },
    'vaquero':{
        'estado':'estado29',
        'val':'^'
    },
    'tilde':{
        'estado':'estado63',
        'val':'~'
    },
    'punto':{
        'estado':'estado12',
        'val':'.'
    },
    'cero':{
        'estado':'estado2',
        'val':'0'
    },
    'guionBajo':{
        'estado':'estado14',
        'val':'_'
    },
    'commillas':{
        'estado':'estado15',
        'val':['"',"'"]
    },
    'reservadas':[
        "auto",
	"break",
	"case",
	"char",
	"const",
	"continue",
	"default",
	"do",
	"double",
	"else",
	"enum",
	"extern",
	"float",
	"for",
	"goto",
	"if",
	"int",
	"long",
	"register",
	"return",
	"short",
	"signed",
	"sizeof",
	"static",
	"struct",
	"switch",
	"typedef",
	"union",
	"unsigned",
	"void",
	"volatile",
	"while"
    ],
    'numeral':{
        'estado':'estado64',
        'val':'#'
    }
}
estadosMap['numeros0'] = estadosMap['numeros']['val'] + ['0']
estadosMap['validosHex'] = estadosMap['numeros0'] + estadosMap['af']
estadosMap['letrasNumeros0_'] = estadosMap['numeros0'] + estadosMap['letras']['val'] + ['_']

class Fuente(object):
    def __init__(self):
        self.linea = 0
        self.columna = 0
        self.archivo = ""
        self.countT = 0
        self.val = ""

    def leerArchivo(self,path):
        filename = open(path,'r')
        self.archivo = filename.read()
        #self.archivo = self.archivo.strip()

    def finalArchivo(self):
        if self.countT < len(self.archivo):
            return False
        return True

    def permitirSiguiente(self):
        self.siguiente = True

    def nextToken(self):
        if self.siguiente:
            self.token = False
            self.siguiente = False
            self.columna += 1
            if self.countT < len(self.archivo):
                self.token = self.archivo[self.countT] 
                self.val += self.token
                self.countT += 1

    def procesarToken(self,t):
        print t,self.linea,self.columna

class Token(object):
    def __init__(self,tipo = False,token = False,linea=0,columna=0):
        self.tipo = tipo
        self.token = token
        self.linea = linea
        self.columna = columna
    
    def info(self):
        if self.tipo == "Error":
            self.infoError()
        else:
            if self.token[-1] == "\n":
                self.token = self.token[0:-1]
            print self.tipo,self.token

    def infoError(self):
        print self.tipo, 'linea:',self.linea,'columna: ',self.columna
        print "TOKEN:",self.token

class Estados(object):
    def __init__(self,fuente):
        self.fuente = fuente
        self.val = ""
        self.estado1()

    def estado1(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        while(self.fuente.token!=False):
            t = self.fuente.token
            tipoToken = Token()
            if t in estadosMap['separador']:
                self.fuente.val = ""
                if t == "\n":
                    self.fuente.linea += 1
                    self.fuente.columna = 0
            else:
                for i in estadosMap:
                    Val = False
                    if 'val' in estadosMap[i]:
                        val = estadosMap[i]['val']
                    if t == val or t in val:
                        if 'estado' in estadosMap[i]:
                            tipoToken = self[estadosMap[i]['estado']]
                            if tipoToken == None:
                                tipoToken = self.clasificaToken('Error')
                            tipoToken.info()
                if not tipoToken.tipo:
                    print "no reconocido",t
            
            if tipoToken.tipo == "Error":
                return False
            
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

        return True

    def estado2(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token in estadosMap['hex']:
            return self.estado4()
        elif self.fuente.token in estadosMap['oct']:
            return self.estado3()
        elif self.fuente.token == '.':
            return self.estado7()
        else:
            return self.return2estado1("Entero")

    def estado3(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        while self.fuente.token not in estadosMap['separador']:
            if not self.fuente.token in estadosMap['oct']:
                return self.return2estado1("Octal",True)
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

        self.fuente.countT -= 1
        return self.return2estado1("Octal",False)

    def estado4(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token in estadosMap['validosHex']:
            return self.estado5()

    def estado5(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        while self.fuente.token not in estadosMap['separador']:
            if not self.fuente.token in estadosMap['validosHex']:
                return self.return2estado1("Hexadecimal",True)
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

        self.fuente.countT -= 1
        return self.return2estado1("Hexadecimal",False)

    def estado6(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        t = self.fuente.token
        while t not in estadosMap['separador']:
            if t in estadosMap['e']:
                return self.estado9()

            if t == '.':
                return self.estado7()

            if not t in estadosMap['numeros0']:
                return self.return2estado1("Enteros")

            self.fuente.permitirSiguiente()
            self.fuente.nextToken()
            t = self.fuente.token

        self.fuente.countT -= 1
        return self.clasificaToken("Enteros")
                
    def return2estado1(self,nombreToken,clear=True):
        if len(self.fuente.val) and clear:
            #si avanzaste para saber el siguiente y reiniciar
            self.fuente.val = self.fuente.val[0:-1]
            tmp = self.clasificaToken(nombreToken)
            self.fuente.countT -= 1
        else:
            #si no avanzas por que es solo 1 como estado55
            tmp = self.clasificaToken(nombreToken)
        self.fuente.val = ""
        return tmp

    def estado7(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token in estadosMap['numeros0']:
            return self.estado8()

    def estado8(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        while self.fuente.token not in estadosMap['separador']:
            if self.fuente.token in estadosMap['e']:
                return self.estado9()
            if not self.fuente.token in estadosMap['numeros0']:
                return self.return2estado1("Flotante",True)
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

        self.fuente.countT -= 1
        return self.clasificaToken("Flotante")

    def estado9(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        t = self.fuente.token
        if t in estadosMap['numeros0']:
            return self.estado11()
        if t in ['+','-']:
            return self.estado10()

    def estado10(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token in estadosMap['numeros0']:
            return self.estado11()

    def estado11(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        while self.fuente.token not in estadosMap['separador']:
            if not self.fuente.token in estadosMap['numeros0']:
                return self.return2estado1("Numero Exponencial",True)
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

        self.fuente.countT -= 1
        return self.clasificaToken("Numero Exponencial")
        
    def estado12(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token in estadosMap['numeros0']:
            return self.estado8()
        return self.return2estado1("Operador",True)

    def estado13(self):
        t = self.fuente.token
        while t not in estadosMap['separador']:
            if not t in estadosMap['letrasNumeros0_']:
                #return self.clasificaToken("Error")
                return self.estado13_1(True)
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()
            t = self.fuente.token
        self.fuente.countT -= 1
        return self.estado13_1()

    def estado13_1(self,clear=False):
        if self.fuente.val[0:-1] in estadosMap['reservadas']:
            return self.return2estado1("Palabra reservada",clear)
        return self.return2estado1("Identificador",clear)

    def estado14(self):
        return self.estado13()
        
    def estado15(self):#estado17
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        t = self.fuente.token
        while not t in estadosMap['commillas']['val']:#cualquiercosa
            if self.fuente.finalArchivo():
                return self.clasificaToken("Error")
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()
            t = self.fuente.token
        return self.return2estado1("String",False)
        
    def estado20(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token != "=":
            return self.return2estado1("Asignacion",True)
        return self.estado55()

    def estado22(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token == '>':
            return self.estado23()
        return self.estado25()

    def estado23(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        return self.estado55()

    def estado25(self):
        return self.estado55()

    def estado26(self):
        return self.return2estado1("Operador",False)

    def estado27(self):
        return self.return2estado1("Abre Corchetes",False)

    def estado28(self):
        return self.return2estado1("Cierra Corchetes",False)

    def estado29(self):
        self.fuente.permitirSiguiente()
        return self.estado55()

    def estado30(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token != '=':
            return self.return2estado1("Negacion",True)
        return self.estado55()
    
    def estado31(self):
        return self.return2estado1('Operador',False)

    def estado32(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token not in ['=','&']:
            return self.return2estado1("Operador",True)

        if self.fuente.token == '=':
            return self.estado33()
        return self.estado34()

    def estado33(self):
        return self.estado55()

    def estado34(self):
        self.fuente.nextToken()
        if self.fuente.token == '&':
            return self.return2estado1('Operador',False)
    
    def estado35(self):
        return self.return2estado1('Apertura de parentesis',False)
    
    def estado36(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token != "=":
            return self.return2estado1("Operador",True)
        return self.estado37()

    def estado37(self):
        #self.fuente.permitirSiguiente()
        return self.estado55()

    def estado38(self):
        return self.return2estado1('Cierre parentesis',False)

    def estado39(self):
        return self.estado55()
    
    def estado40(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token not in ['+','=']:
            return self.return2estado1("Operador",True)
        if self.fuente.token == "=":
            return self.estado39()
        return self.estado41()

    def estado41(self):
        if self.fuente.token == "+":
            return self.return2estado1("Operador",False)

    def estado42(self):
        return self.return2estado1("Operador",False)

    def estado43(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        t = self.fuente.token

        if t == "=":
            return self.estado44()
        elif t == "-":
            return self.estado45()
        elif t == ">":
            return self.estado46()
        else:
            return self.return2estado1("Operador",True)

    def estado44(self):
        return self.estado55()

    def estado45(self):
        return self.return2estado1("Operador",False)

    def estado46(self):
        return self.return2estado1("Operador",False)

    def estado47(self):
        return self.return2estado1("Operador",False)

    def estado48(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        t = self.fuente.token
        if t == "=":
            return self.estado49()
        elif t == "*":
            return self.estado48_1()
        elif t == "/":
            return self.estado48_2()
        else:
            return self.return2estado1("Operador",True)

    def estado48_1(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        anterior = self.fuente.token
        while True:
            if self.fuente.token == "\n":
                self.fuente.linea+=1
                self.fuente.columna = 0
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()

            if anterior == "*" and self.fuente.token == "/":
                return self.return2estado1("Comentario",False)

            anterior = self.fuente.token

            if self.fuente.finalArchivo():
                return self.clasificaToken("Error")

    def estado48_2(self):
        while True:
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()
            t = self.fuente.token
            if t == "\n" or self.fuente.finalArchivo():
                self.fuente.countT -=1#se restaura al siguiente salto
                self.fuente.val = self.fuente.val[0:-1]
                return self.clasificaToken("Comentario")



    def estado49(self):
        return self.estado55()

    def estado50(self):
        return self.return2estado1('Operador',False)

    def estado51(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token == "<":
            return self.estado52()
        elif self.fuente.token == "=":
            return self.estado53()
        else:
            return self.return2estado1("Operador",True)
    
    def estado52(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token != '=':
            return self.return2estado1("Operador",True)
        return self.estado55()

    def estado53(self):
        return self.estado55()

    def estado55(self):#estado55,estado33,estado37,estado39,44,49,53,60
        self.fuente.nextToken()
        if self.fuente.token == estadosMap['igual']['val']:
            return self.return2estado1("Operador",False)

    def estado58(self):
        return self.return2estado1("Apertura de llave",False)

    def estado59(self):
        self.fuente.permitirSiguiente()
        self.fuente.nextToken()
        if self.fuente.token == "|":
            return self.estado61()
        elif self.fuente.token == "=":
            return self.estado60()
        else:
            return self.return2estado1("Operador",True)

    def estado60(self):
        return self.estado55()
            
    def estado61(self):
        return self.return2estado1("Operador",False)

    def estado62(self):
        return self.return2estado1("Cierre de llave",False)

    def estado63(self):
        return self.return2estado1("Operador",False)

    ##faltantes
    def estado64(self):
        while True:
            self.fuente.permitirSiguiente()
            self.fuente.nextToken()
            t = self.fuente.token
            if t == "\n" or self.fuente.finalArchivo():
                self.fuente.countT -=1#se restaura al siguiente salto
                self.fuente.val = self.fuente.val[0:-1]
                return self.clasificaToken("tipo #")

    def __getitem__(self,name):
        if hasattr(self,name):
            temp = getattr(self,name)
            return temp()

    def clasificaToken(self,nombre):
        nameC =  sys._getframe().f_back.f_code.co_name
        if nombre == "Error":
            print 'invoce',nameC
            return Token("Error",self.fuente.val,linea=self.fuente.linea,columna=self.fuente.columna)
        return Token(nombre,self.fuente.val)
        
fuente = Fuente()
fuente.leerArchivo("c2.c")
estado = Estados(fuente)
