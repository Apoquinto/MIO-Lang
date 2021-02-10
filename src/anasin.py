import sys
def initAnasin(dirFile):
    file = open(dirFile)

    #Banderas para identificar estructuras
    counter=0
    fPROG=False
    fID=False
    fSI=False
    fREP=False
    fIMP=False
    fLEE=False
    fERROR=False
    fOP_AR=False
    fOP_REL=False

    #Pila
    stack=[]
    def lastItem():
        return stack[len(stack)-1]

    #Pasamos a la mainStack todas las lineas del codigo
    mainStack = []
    for line in file:
        print(line, end = '')
    line = line.split()
    mainStack.append(line)
    print()

    #Recorremos todos los elementos del mainStack
    for line in mainStack:
        counter += 1
        # PROG
        if 'PROGRAMA' in line and not(fPROG):
            fPROG=True
            stack.append('FINPROG') 
            stack.append('SENTS')
            stack.append('[id]')
            continue
        if '[id]' in line and lastItem()=='[id]' and fPROG:
            if not(fERROR):
                stack.pop()
                continue
            else:
                fERROR=True
                break
        if 'FINPROG' in line and fPROG and lastItem()=='FINPROG':
            fPROG=False
            stack.pop()
            continue
    
        # SENTS
        if lastItem()=='SENTS':
            stack.pop()
            stack.append('SENT')  

        # COMPARA
        if fOP_REL or (lastItem()=='COMPARA' and fSI):
            if '[id]' in line:      
                stack.pop()
                fOP_REL=True
                stack.append('[op_rel]')
                continue
            elif lastItem()=='[op_rel]' and ('<' in line or '>' in line) and fSI and fOP_REL:    
                fOP_REL=False
                stack.pop()
                stack.append('ELEM')      
            else:
                fERROR=True
                break

        # op_ar
        elif (fOP_AR and '[op_ar]' in line):
            stack.append('ELEM')
            continue

        # ELEM
        elif lastItem()=='ELEM':
            if '[val]' in line or '[id]' in line:
                stack.pop()
                if not(fSI):
                    if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                        stack.append('SENTS')     
                if '[op_ar]' in mainStack[counter]:   
                    fOP_AR=True
                    continue
                else:
                    fID=False
                    continue
            else:
                fERROR=True
                break
                
        # SENT 
        elif lastItem()=='SENT' or fID or fSI or fREP or fIMP or fLEE:
            if ('=' in line and lastItem()=='=' and fID) or fID and lastItem()=='SENT' and not(fIMP):
                stack.pop()     
                fID=False
            elif ('[id]' in line and lastItem()=='SENT') and not(fIMP):      
                stack.pop()     
                stack.append('ELEM')
                stack.append('=')
                fID=True 
                continue
            elif 'SI' in line or fSI and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line) and not('REPITE' in line): 
                if 'SI' in line and lastItem()=='SENT':
                    stack.pop()        
                    stack.append('FINSI')
                    stack.append('SENTS')     
                    stack.append('ENTONCES')
                    stack.append('COMPARA') 
                    fSI=True  
                    continue
                if lastItem()=='ENTONCES' and fSI:
                    if 'ENTONCES' in line:          
                        stack.pop()
                        continue
                    else:
                        fERROR=True
                        break
                if 'SINO' in line and fSI:    
                    stack.append('SENTS')      
                    continue
                if fSI and lastItem()=='FINSI':
                    if 'FINSI' in line:
                        stack.pop()
                        if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                            stack.append('SENTS') 
                        if not('FINSI' in stack):
                            fSI=False
                            continue
                        else:
                            continue
                    else:
                        fERROR=True
                        break
            
            elif 'REPITE' in line or fREP and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line): 
                if 'REPITE' in line and lastItem()=='SENT':
                    stack.pop()
                    fREP=True
                    stack.append('FINREP')
                    stack.append('SENTS')     
                    stack.append('VECES')  
                    stack.append('ELEM')      
                    continue 
                if lastItem()=='VECES' and fREP:
                    if 'VECES' in line:          
                        stack.pop()
                        continue
                    else:
                        fERROR=True
                        break
                if lastItem()=='FINREP' and fREP:
                    if 'FINREP' in line:
                        stack.pop()
                        if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                            stack.append('SENTS') 
                        if not('FINREP' in stack):
                            fREP=False
                            continue
                        else:
                            continue
                    else:
                        fERROR=True
                        break

                        
            elif 'IMPRIME' in line or fIMP:
                if 'IMPRIME' in line and lastItem()=='SENT':
                    stack.pop()
                    fIMP=True
                    stack.append('IMPRIME')
                    continue
            if lastItem()=='IMPRIME' and fIMP:
                if '[txt]' in line:
                    fIMP=False
                    stack.pop()
                    if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                        stack.append('SENTS') 
                    continue
                elif '[id]' in line or '[val]' in line:
                    stack.pop()
                    stack.append('ELEM')     
                    fIMP=False
                    stack.pop()
                    if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                        stack.append('SENTS') 
                else:
                    fERROR=True
                    break

            elif 'LEE' in line or fLEE: 
                if 'LEE' in line and lastItem()=='SENT':        
                    stack.pop()          
                    stack.append('LEE')
                    fLEE=True
                    continue
                if lastItem()=='LEE' and fLEE:
                    if '[id]' in line:              
                        stack.pop()
                        fLEE=False                 
                        if ('[id]' in mainStack[counter] or 'SI' in mainStack[counter] or 'REPITE' in mainStack[counter] or 'IMPRIME' in mainStack[counter] or 'LEE' in mainStack[counter]):
                            stack.append('SENTS')
                            continue
                    else:
                        fERROR=True
                        break
            else:
                fERROR=True
                break
        else:
            fERROR=True
            break  

    # Verificacion final
    if fERROR:
        print('COMPILACION ERRONEA')
    elif stack==[]:
        print('COMPILACION EXITOSA')
    else:
        print('COMPILACION ERRONEA')

    file.close()