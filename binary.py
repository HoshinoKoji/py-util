def find_keyword(infile, outfile, target):
    fr = open(infile, 'rb')
    found = False
    offset = 0
    try:
        while not found:
            fr.seek(offset)
            particle = fr.read(len(target))
            if particle == target:
                found = True
            else:
                offset += 1
        fw = open(outfile, 'wb')
        fr.seek(0)
        fw.write(fr.read(offset + 100))
        fw.close()
    except:
        pass
    finally:
        fr.close()