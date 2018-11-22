#coding: utf-8
import sys

def read_varint(fd):
    """
    Cette fonction lit un entier de taille variable dans un file descriptor passé en paramètre, accordément à la spec suivante
    https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer
    """
    first_byte = fd.read(1)
    first = int.from_bytes(first_byte, 'big')
    if first < 0xfd:
        return first_byte
    elif first == 0xfd:
        return fd.read(2)
    elif first == 0xfe:
        return fd.read(4)
    elif first == 0xff:
        return fd.read(8)
    else:
        raise Exception('Could not read varint from file descriptor')

def parse_genesis(file):
    # Le dictionnaire qui contiendra les infos du bloc
    genesis = {}
    # On ouvre le fichier .dat
    with open(file, 'rb') as f:
        # On lit tant qu'on a pas les magic bytes, signe du début du bloc
        while True:
            magic = f.read(4)
            if int.from_bytes(magic, 'big') == 0xfdc2b8dd:
                # On a lu les magic bytes, on est dans le bloc
                break
        print('Je lis le header :')
        print('     Je lis la taille du header')
        genesis['header_length'] = f.read(4)
        print('     Je lis la version du bloc')
        genesis['version'] = f.read(4)
        print('     Je lis le hash du block précédent')
        genesis['prev_hash'] = f.read(32)
        print('     Je lis la merkle root')
        genesis['merkle'] = f.read(32)
        print('     Je lis le timestamp')
        genesis['timestamp'] = f.read(4)
        print('     Je lis la target')
        genesis['target'] = f.read(4)
        print('     Je lis le nonce')
        genesis['nonce'] = f.read(4)
        print('     Je lis le nombre de transactions (un varint)')
        genesis['txcount'] = read_varint(f)
        print('\n\nJe lis les  transactions')
        genesis['transactions'] = []
        for i in range(int.from_bytes(genesis['txcount'], 'big')):
            genesis['transactions'].append({})
            print(' Je lis la première transaction')
            print('     Je lis la version de la transaction')
            genesis['transactions'][i]['version'] = f.read(4)
            print('     Je lis le nombre d\'inputs de la tx (un varint)')
            genesis['transactions'][i]['input_count'] = read_varint(f)
            print('\n     Je lis les inputs de la transactions')
            genesis['transactions'][i]['inputs'] = []
            for j in range(int.from_bytes(genesis['transactions'][i]['input_count'], 'big')):
                genesis['transactions'][i]['inputs'].append({})
                print('         Je lis le premier input')
                print('             Je lis le hash de la transaction ayant créé cet input')
                genesis['transactions'][i]['inputs'][j]['hash'] = f.read(32)
                print('             Je lis l\'index de l\'input dans cette transaction')
                genesis['transactions'][i]['inputs'][j]['txindex'] = f.read(4)
                print('             Je lis la taille du script (un varint)')
                genesis['transactions'][i]['inputs'][j]['script_length'] = read_varint(f)
                print('             Je lis le bytecode du script')
                genesis['transactions'][i]['inputs'][j]['script'] = f.read(int.from_bytes(genesis['transactions'][i]['inputs'][j]['script_length'], 'big'))
                print('             Je lis la sequence')
                genesis['transactions'][i]['inputs'][j]['sequence'] = f.read(4)
            print('\n       J\'ai fini de lire les inputs !')
            print('         Je lis le nombre d\'outputs (un varint)')
            genesis['transactions'][i]['output_count'] = read_varint(f)
            genesis['transactions'][i]['outputs'] = []
            for j in range(int.from_bytes(genesis['transactions'][i]['output_count'], 'big')):
                genesis['transactions'][i]['outputs'].append({})
                print('         Je lis le premier ouput')
                print('             Je lis la valeur (en satoshis) de l\'output')
                genesis['transactions'][i]['outputs'][j]['value'] = f.read(8)
                print('             Je lis la taille du script (un varint)')
                genesis['transactions'][i]['outputs'][j]['script_length'] = read_varint(f)
                print('             Je lis le script')
                genesis['transactions'][i]['outputs'][j]['script'] = f.read(int.from_bytes(genesis['transactions'][i]['outputs'][j]['script_length'], 'big'))
            print('\n       J\'ai fini de lire les outputs !')
            print('     Je lis le locktime de la transaction')
            genesis['transactions'][i]['lock_time'] = f.read(4)
        print('\nJ\'ai fini de lire les transactions !!!!!')
        print('Bon bah j\'ai fini de lire le bloc')
        f.close()
    return genesis

def display_block(block):
    """
    block : un json
    """
    print('========================================================================')
    print('========================================================================')
    print('||                             HEADER                                 ||')
    print('||====================================================================||')
    print('||                   Taille : {} octets                        ||'.format(int.from_bytes(block['header_length'], 'big')))
    print('||                   Version : {}                               ||'.format(int.from_bytes(block['version'], 'big')))
    print('||                   Prev hash : {}                                    ||'.format(int.from_bytes(block['prev_hash'], 'big')))
    print('||Merkle root : {}||'.format(int.from_bytes(block['merkle'], 'big')))
    print('||                   Timestamp : {}                            ||'.format(int.from_bytes(block['timestamp'], 'big')))
    print('||                   Target : {}                              ||'.format(int.from_bytes(block['target'], 'big')))
    print('||                   Nonce : {}                               ||'.format(int.from_bytes(block['nonce'], 'big')))
    print('||====================================================================||')
    print('||                           TRANSACTIONS                             ||')
    print('||====================================================================||')      
    for i in range(int.from_bytes(block['txcount'], 'big')):
        print('||Transaction {} :                                                     ||'.format(i))
        print('||	version : {}                                            ||'.format(int.from_bytes(block['transactions'][i]['version'], 'big')))
        for j in range(int.from_bytes(block['transactions'][i]['input_count'], 'big')):
            print('||   input {} :                                                        ||'.format(j))
            print('||		hash : {}                                              ||'.format(int.from_bytes(block['transactions'][i]['inputs'][j]['hash'], 'big')))
            print('||       txindex : {}               	                      ||'.format(int.from_bytes(block['transactions'][i]['inputs'][j]['txindex'], 'big')))
            print('||       script : {}        ||'.format(block['transactions'][i]['inputs'][j]['script']))
            print('||       sequence : {}                                        ||'.format(int.from_bytes(block['transactions'][i]['inputs'][j]['sequence'], 'big')))
        for j in range(int.from_bytes(block['transactions'][i]['output_count'], 'big')):
            print('||	output {} :                                                    ||'.format(j))
            print('||		value : {} satoshis                    ||'.format(int.from_bytes(block['transactions'][i]['outputs'][j]['value'], 'big')))
            print('||		script : {}         ||'.format(block['transactions'][i]['outputs'][j]['script']))
            print('||	locktime : {}                                                  ||'.format(int.from_bytes(block['transactions'][i]['lock_time'], 'big')))
            print('||                                                                    ||')
        print('========================================================================')
        print('========================================================================')
	
	
if __name__ == '__main__':
	if len(sys.argv) == 2:
		genesis = parse_genesis(sys.argv[1])
		print('\n')
		print('On a fini de lire le block, on l\'affiche')
		print('\n\n')
		display_block(genesis)

