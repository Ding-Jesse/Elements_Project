# $ LINE OBJECT LOADS
#   LINELOAD  "B1"  "STORY4"  TYPE "TRAPF"  DIR "GRAV"  LC "LIVE"  FSTART 10  FEND 10  RDSTART 0  RDEND 3.472222E-02
# $ STATIC LOADS
#   LOADCASE "DEAD"  TYPE  "DEAD"  SELFWEIGHT  1
#   LOADCASE "LIVE"  TYPE  "LIVE"  SELFWEIGHT  0
import re
import numpy as np
def _is_right_version(checking, words):
    if checking == '$ PROGRAM INFORMATION' and words[0] == 'PROGRAM':
        if words[1] != '"ETABS"':
            print('PROGRAM should be "ETABS"')
        if words[3] != '"9.7.3"':
            print('VERSION should be "9.7.3"')


def _is_right_unit(checking, words):
    if checking == '$ CONTROLS' and words[0] == 'UNITS':
        if words[1] != '"TON"' and words[2] != '"M"':
            print('UNITS should be "TON"  "M"')



def _load_e2k(read_file):
    with open(read_file, encoding='big5',errors='replace') as path:
        content = path.readlines()
        content = [x.strip() for x in content]

    return content


def load_e2k(read_file):
    """ load e2k file
    """
    content = _load_e2k(read_file)

    point_coordinates = {}
    lines = {}
    materials = {}
    sections = {}
    for line in content:
        # 正規表達式，轉換多格成一格，因為 ETABS 自己好像也不管
        line = re.sub(' +', ' ', line)
        words = np.array(line.split(' '))
        # checking 是不容易變的
        if words[0] == '$':
            checking = line

        _is_right_version(checking, words)
        _is_right_unit(checking, words)
    return

def write_e2k(df,read_file,output_path,output_name):
    content = _load_e2k(read_file)
    path = output_path + output_name
    f = open(path, 'w')
    df = df.reset_index()
    isAswrite = False
    isCasewrite = False
    checking = ''
    topAS_load_case_name = 'TopAs'
    botAS_load_case_name = 'BotAs'
    shear_load_case_name = 'Avs'
    for line in content:

        line = re.sub(' +', ' ', line)
        words = np.array(line.split(' '))
        _is_right_version(checking, words)
        _is_right_unit(checking, words)
        if checking == '$ LINE OBJECT LOADS' and not isAswrite:
            for index, row in df.iterrows():
                if row[("編號","")] == '': continue
                beam_length = row[("梁長","")]
                start_pos = row[("支承寬","左")]/row[("梁長","")]
                end_pos = 1 - row[("支承寬","右")]/row[("梁長","")]
                
                # 寫入上層主筋
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{topAS_load_case_name}"  FSTART {row[("主筋","左上As")]}  FEND {row[("主筋","左上As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋長度","左1")]/beam_length}'
                f.write(new_line)
                f.write('\n')
                start_pos = start_pos + row[("主筋長度","左1")]/beam_length
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{topAS_load_case_name}"  FSTART {row[("主筋","中上As")]}  FEND {row[("主筋","中上As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋長度","中")]/beam_length}'
                f.write(new_line)
                f.write('\n')
                start_pos = start_pos + row[("主筋長度","中")]/beam_length
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{topAS_load_case_name}"  FSTART {row[("主筋","右上As")]}  FEND {row[("主筋","右上As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋長度","右1")]/beam_length}'
                f.write(new_line)
                f.write('\n')
                
                # 寫入下層主筋  
                start_pos = row[("支承寬","左")]/row[("梁長","")]
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{botAS_load_case_name}"  FSTART -{row[("主筋","左下As")]}  FEND -{row[("主筋","左下As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋","左下長度")]/beam_length}'
                f.write(new_line)
                f.write('\n')
                start_pos = start_pos + row[("主筋","左下長度")]/beam_length
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{botAS_load_case_name}"  FSTART -{row[("主筋","中下As")]}  FEND -{row[("主筋","中下As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋","中下長度")]/beam_length}'
                f.write(new_line)
                f.write('\n')
                start_pos = start_pos + row[("主筋","中下長度")]/beam_length
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{botAS_load_case_name}"  FSTART -{row[("主筋","右下As")]}  FEND -{row[("主筋","右下As")]}  RDSTART {start_pos}  RDEND {start_pos + row[("主筋","右下長度")]/beam_length}'
                f.write(new_line)
                f.write('\n')

                # 寫入箍筋
                start_pos = row[("支承寬","左")]/row[("梁長","")]
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{shear_load_case_name}"  FSTART {row[("箍筋","左Avs")]}  FEND -{row[("箍筋","左Avs")]}  RDSTART {start_pos}  RDEND {start_pos + row[("箍筋長度","左")]/beam_length}'
                f.write(new_line)
                f.write('\n')

                start_pos = start_pos + row[("箍筋長度","左")]/row[("梁長","")]
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{shear_load_case_name}"  FSTART {row[("箍筋","中Avs")]}  FEND -{row[("箍筋","中Avs")]}  RDSTART {start_pos}  RDEND {start_pos + row[("箍筋長度","中")]/beam_length}'
                f.write(new_line)
                f.write('\n')

                start_pos = start_pos + row[("箍筋長度","中")]/row[("梁長","")]
                new_line = f'   LINELOAD  "{row[("編號","")]}"  "{row[("樓層","")]}"  TYPE "TRAPF"  DIR "GRAV"  LC "{shear_load_case_name}"  FSTART {row[("箍筋","右Avs")]}  FEND -{row[("箍筋","右Avs")]}  RDSTART {start_pos}  RDEND {start_pos + row[("箍筋長度","右")]/beam_length}'
                f.write(new_line)
                f.write('\n')
            isAswrite = True
        if checking == '$ STATIC LOADS' and not isCasewrite:
            new_line = f'  LOADCASE "{topAS_load_case_name}"  TYPE  "OTHER"  SELFWEIGHT  0'
            f.write(new_line)
            f.write('\n')
            new_line = f'  LOADCASE "{botAS_load_case_name}"  TYPE  "OTHER"  SELFWEIGHT  0'
            f.write(new_line)
            f.write('\n')
            new_line = f'  LOADCASE "{shear_load_case_name}"  TYPE  "OTHER"  SELFWEIGHT  0'
            f.write(new_line)
            f.write('\n')
            isCasewrite = True
        if words[0] == '$':
            checking = line

        f.write(line)
        f.write('\n')
    f.close()
    return