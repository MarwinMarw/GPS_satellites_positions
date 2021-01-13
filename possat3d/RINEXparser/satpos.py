import numpy as np

GM = 3.986005*np.power(10.0,14)
c = 2.99792458*np.power(10.0,8)
omegae_dot = 7.2921151467*np.power(10.0,-5)

def split_neg_num(number, start_index=0):
    index_minus = number.find('-', start_index)
    fixed = []

    if index_minus > 0 and not number[index_minus-1].isalpha():
        num1 = number[:index_minus]
        num2 = number[index_minus:]

        fixn1 = split_neg_num(num1)
        fixn2 = split_neg_num(num2)
        
        if fixn1 is None:
            fixed.append(num1)
        else:
            for i in fixn1:
                fixed.append(i)

        if fixn2 is None:
            fixed.append(num2)
        else:
            for i in fixn2:
                fixed.append(i)

        return fixed
    else:    
        if index_minus != -1:
            return split_neg_num(number, index_minus+1)
        else:
            return None


def readRinexN(file):
    data = {}
    with open(file,'rt') as f:
        foundend = 0
        idx = 0
        for line in f:
            a = line.split(' ')
            if 'END' in a:
                foundend = 1
                continue
            if foundend==0:
                continue
            b = [x for x in a if x!='']

            fixed_b = [split_neg_num(x) for x in b]
            new_b = []
            
            for i, fb_i in enumerate(fixed_b):
                if fb_i is None:
                    new_b.append(b[i])
                else:
                    for fi in fb_i:
                        new_b.append(fi)

            b = new_b    


            try:
                b.remove('\n')
            except:
                pass
            if len(b)!=4:
                idx += 1
                data[str(idx)] = b
            else:
                for each in b:
                    data[str(idx)].append(each)
                    
    data2 = np.zeros([len(data),38])
    outercount = 0
    for (k,v) in data.items(): 
        count = 0
        for each in v:
            if 'D' in each:
                tmp = each.split('D')
                tmp = float(tmp[0])*np.power(10.0,float(tmp[1]))
            else:
                tmp = float(each)
            data2[outercount,count] = tmp
            count += 1
        outercount += 1
    return data, data2

def readRinexN302(file):
    data = {}
    with open(file,'rt') as f:
        foundend = 0
        idx = 0
        for line in f:
            a = line.split(' ')
            if 'END' in a:
                foundend = 1
                continue
            if foundend==0:
                continue
            b = [ x for x in a if x!='']
            
            fixed_b = [split_neg_num(x) for x in b]
            new_b = []
            
            for i, fb_i in enumerate(fixed_b):
                if fb_i is None:
                    new_b.append(b[i])
                else:
                    for fi in fb_i:
                        new_b.append(fi)

            b = new_b            
            
            try:
                b.remove('\n')
            except:
                pass
            if len(b)!=4:
                idx += 1
                data[str(idx)] = b
            else:
                for each in b:
                    data[str(idx)].append(each)
                    
    data2 = np.zeros([len(data),38])
    outercount = 0
    for (k,v) in data.items(): 
        count = 0
        for each in v:
            if 'D' in each:
                tmp = each.split('D')
                tmp = float(tmp[0])*np.power(10.0,float(tmp[1]))
            else:
                if 'G' in each:
                    tmp = float(each.split('G')[1])
                elif 'C' in each:
                    tmp = float(each.split('C')[1])
                else:
                    tmp = float(each)
            data2[outercount,count] = tmp
            count += 1
        outercount += 1
    return data, data2

def calSatPos(data, timeCor=False, iteration='Newton'):
    sats = np.zeros([data.shape[0],5])
    for j in range(data.shape[0]):
        
        ## load variables
        A = np.power(data[j,17],2) 
        toe = data[j,18] # Time of Ephemeris
        tsv = data[j,18]
        tk = tsv - toe
        try:
            n0 = np.sqrt(GM/np.power(A,3))
        except Exception as e:
            print(e)
            continue
        dn = data[j,12]
        n = n0 + dn
        m0 = data[j,13]
        M = m0+n*tk
        
        af0 = data[j,7]
        af1 = data[j,8]
        w = data[j,24]
        cuc = data[j,14] 
        cus = data[j,16]
        crc = data[j,23]
        crs = data[j,11]
        i0 = data[j,22]
        idot = data[j,26]
        omg0 = data[j,20]
        odot = data[j,25] 
        e = data[j,15] # Eccentricity
        
        ## time correction
        if timeCor == True:
            NRnext = 0
            NR = 1
            m = 1
            while np.abs(NRnext-NR)>np.power(10.0,-16):
                NR = NRnext
                f = NR-e*np.sin(NR)-M
                f1 = 1-e*np.cos(NR)
                f2 = e*np.sin(NR)
                if iteration=='Householder':
                    NRnext = NR - f/(f1-(f2*f/(2*f1)))
                else:
                    NRnext = NR - f/f1
                m += 1
            
            E = NRnext
            
            F = -2*np.sqrt(GM)/np.power(c,2)
            delta_tr = F*e*np.sqrt(A)*np.sin(E)
            delta_tsv = af0+af1*(tsv-toe)+delta_tr
            t = tsv-delta_tsv
            tk = t-toe
            M = m0+n*tk
        
        NRnext = 0
        NR = 1
        m = 1
        while np.abs(NRnext-NR)>np.power(10.0,-16):
            NR = NRnext
            f = NR-e*np.sin(NR)-M
            f1 = 1-e*np.cos(NR)
            f2 = e*np.sin(NR)
            if iteration=='Householder':
                NRnext = NR - f/(f1-(f2*f/(2*f1)))
            else:
                NRnext = NR - f/f1
            m += 1
    
        E = NRnext
        v = np.arctan2(np.sqrt(1-np.power(e,2))*np.sin(E),np.cos(E)-e)
        phi = v + w
        u = phi + cuc*np.cos(2*phi) + cus*np.sin(2*phi)
        r = A*(1-e*np.cos(E)) + crc*np.cos(2*phi) + crs*np.sin(2*phi)
        i = i0 + idot*tk
        Omega = omg0 + (odot-omegae_dot)*tk - omegae_dot*toe
        x1 = np.cos(u)*r
        y1 = np.sin(u)*r
        
        sats[j,0] = data[j,0]
        sats[j,1] = x1*np.cos(Omega) - y1*np.cos(i)*np.sin(Omega)
        sats[j,2] = x1*np.sin(Omega) + y1*np.cos(i)*np.cos(Omega)
        sats[j,3] = y1*np.sin(i)
    return sats


def process_RINEX_file(filename):
    rawdata,data = readRinexN302(filename)
    satp = calSatPos(data)
    satell = dict()
    for each in satp:
        satell[format(np.uint8(each[0]),'2d')] = []
        for i in each[1:-1]:
            if str(i) == 'nan':
                del satell[format(np.uint8(each[0]),'2d')]
                break
            satell[format(np.uint8(each[0]),'2d')].append(float(i))
        

    return satell
