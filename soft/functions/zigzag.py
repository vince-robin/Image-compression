import numpy as np
import matplotlib.pyplot as plt


def zigzag(input):

    h = 0
    v = 0
    v_min = 0
    h_min = 0
    v_max = input.shape[0]
    h_max = input.shape[1]
    i = 0
    output = np.zeros((v_max * h_max))

    while (v < v_max) and (h < h_max):

        if ((h + v) % 2) == 0:  
            if v == v_min:
                output[i] = input[v, h]  
                if h == h_max:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == h_max - 1) and (v < v_max):  
                output[i] = input[v, h]
                v = v + 1
                i = i + 1
            elif (v > v_min) and (h < h_max - 1): 
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1
        else:

            if (v == v_max - 1) and (h <= h_max - 1):  
                output[i] = input[v, h]
                h = h + 1
                i = i + 1
            elif h == h_min:  
                output[i] = input[v, h]
                if v == v_max - 1:
                    h = h + 1
                else:
                    v = v + 1
                    i = i + 1
            elif (v < v_max - 1) and (h > h_min):  
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1

        if (v == v_max - 1) and (h == h_max - 1):  
            output[i] = input[v, h]
            break

    return output


def inverse_zigzag(input, vmax, hmax):
		
	h = 0
	v = 0
	vmin = 0
	hmin = 0
	output = np.zeros((vmax, hmax))
	i = 0

	while ((v < vmax) and (h < hmax)): 
		if ((h + v) % 2) == 0:                 
			if (v == vmin):				
				output[v, h] = input[i]        
				if (h == hmax):
					v = v + 1
				else:
					h = h + 1                        
				i = i + 1
			elif ((h == hmax -1 ) and (v < vmax)):   
				output[v, h] = input[i] 
				v = v + 1
				i = i + 1
			elif ((v > vmin) and (h < hmax -1 )):    
				output[v, h] = input[i] 
				v = v - 1
				h = h + 1
				i = i + 1
		else:                                    
			if ((v == vmax -1) and (h <= hmax -1)):       
				output[v, h] = input[i] 
				h = h + 1
				i = i + 1
			elif (h == hmin):                  
				output[v, h] = input[i] 
				if (v == vmax -1):
					h = h + 1
				else:
					v = v + 1
				i = i + 1        		
			elif((v < vmax -1) and (h > hmin)):   
				output[v, h] = input[i] 
				v = v + 1
				h = h - 1
				i = i + 1

		if ((v == vmax-1) and (h == hmax-1)):          
			output[v, h] = input[i] 
			break

	return output


def viewing_zigzag_table(vmax, hmax, out_dir):
        
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    zigzag_table = np.zeros((vmax, hmax))
    i = 0

    while ((v < vmax) and (h < hmax)): 
        if ((h + v) % 2) == 0:                
            if (v == vmin):				
                zigzag_table[v, h] = i       
                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        
                i = i + 1
            elif ((h == hmax -1 ) and (v < vmax)):   
                zigzag_table[v, h] = i 
                v = v + 1
                i = i + 1
            elif ((v > vmin) and (h < hmax -1 )):   
                zigzag_table[v, h] = i 
                v = v - 1
                h = h + 1
                i = i + 1
        else:                                    
            if ((v == vmax -1) and (h <= hmax -1)):       
                zigzag_table[v, h] = i 
                h = h + 1
                i = i + 1
            elif (h == hmin):                 
                zigzag_table[v, h] = i 
                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1        		
            elif((v < vmax -1) and (h > hmin)):   
                zigzag_table[v, h] = i 
                v = v + 1
                h = h - 1
                i = i + 1

        if ((v == vmax-1) and (h == hmax-1)):          
            zigzag_table[v, h] = i 
            break          
    
    fig, ax = plt.subplots()
    ax.matshow(zigzag_table, cmap='viridis')
    for (i, j), z in np.ndenumerate(zigzag_table):
        ax.text(j, i, int(z), ha='center', va='center', color='black')
    plt.title("Zigzag-table")

    plt.savefig(out_dir+"zigzag_table.png")
