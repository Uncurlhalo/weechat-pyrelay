int swap_endian_int(char* buf)
{
    return (buf[3] << 24) | (buf[2] << 16) | (buf[1] << 8) | buf[0]; 
}

char* decode(char* buf)
{
    char type[3];
    
    int length = swap_endian_int(buf);
    buf += 4;
    int compression = *buf++;
    
    strncpy(type, buf, 3);
    buf += 3;
    
    return buf;
}
