import struct

class FF6Font(object):
	
	def __init__(self,rawdata):
		#input data validation
		if not isinstance(rawdata,bytearray):
			raise NameError('Data must be bytearray')
		if rawdata[:4]!='FONT':
			raise NameError('Signature FONT dose not found')
		#parameters initiation
		self.__rawdata=rawdata		#Raw data loading
		self.__nRows=rawdata[4]		#number of rows in symbol (byte) 
		self.__nSymbols=rawdata[6]+0x100*rawdata[7] #number of symbols in font (word)
		self.__EOS=rawdata[8] #End of string symbol


		#get alphabet
		self.__alphabet=[]			#initiation of alphabet tuple
		pos=0x0A		#go to relative position 0x000A 
		while(1):
			symbol=	rawdata[pos]+0x100*rawdata[pos+1]	#read symbol number (word) from raw data
			pos+=2
			if symbol==0xFFFF:	break					#till we find end marker (0xFFFF) 
			else:
				self.__alphabet.append(symbol)			#add symbol to alphabet

		#get pointer page	
		self.__ptrpage=struct.unpack_from('L'*self.__nSymbols,rawdata,pos)			#read long pointers PTR to symbols in font from position after alphabet
#		for i in range(self.__nSymbols):			#for all symbols in font (nSymbols)
#			ptr=0
#			for nbyte in range(4):					#sequentially read dword (4 bytes) pointers
#				ptr+=(0x100**nbyte)*rawdata[pos+i*4+nbyte]
#			self.__ptrpage.append(ptr)

	def getptrpage(self):			#return tuple with pointers on symbols sprites (real position of the beginning of sprite header is PTR-4)
		return self.__ptrpage

	def getalphabet(self):			#return tuple of symbols in alphabet
		return self.__alphabet
		
	def getfontprops(self):			#return font properties
		return {"nRows":self.__nRows,"nSymbols":self.__nSymbols}

	def getEOSsymbol(self):			#return End of string symbol
		return self.__EOS
		
	def getfontsymbol(self,rawsprite,nColumns,palette):
		symbol=[]
		iRow=0
		for iRow in range(self.__nRows): #symbol for every row in symbol
			row=[]        
			for col in range(nColumns): #for every column in row (one column = one byte) 			
				pos=iRow*nColumns+col	#calc of current column position
				for npix in range(4):   #for every pixel in current column  (4 pixels in one byte/column)    
					color=(rawsprite[pos]>>npix*2)&0x03  #get pixel color (left pixel corresponds to first two less significants bits) 
					if len(palette)>0: row.append(palette[color])   #if palette is defined add pixel to row
					else: row.append(color)   #add pixel to row
			symbol.append(row)                 #add row to symbol
		return symbol	

	def getsymbols(self,**kwargs):
		palette=kwargs.get('palette',[])	#load palette if exists
		result=[]		
		for i in range(self.__nSymbols):
			pos=self.__ptrpage[i]-4		
			rawsymbol=[]			
			#read symbol header (width of symbol in pixels and columns)
			nPixels=self.__rawdata[pos] #get width of symbol in pixels
			nColumns=self.__rawdata[pos+1]	#get width of symbol in column
			pos+=2
			if (nColumns>0): 
				sprite_size=self.__nRows*nColumns #size of symbol sprite in bytes
				rawsprite=self.__rawdata[pos:pos+sprite_size]	#get bytes of symbol sprite from font data
				pos+=sprite_size
				result.append({"columns":nColumns,"pixels":nPixels,"symbol":self.getfontsymbol(rawsprite,nColumns,palette)})	#append symbol to results 
			else:
				result.append({"columns":nColumns,"pixels":nPixels,"symbol":[]})   #append empty symbol to results
		return result	




