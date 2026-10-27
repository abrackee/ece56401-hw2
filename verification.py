
import ctypes, ctypes.util
lib = ctypes.CDLL(ctypes.util.find_library("crypt"))
lib.crypt.restype = ctypes.c_char_p
lib.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

password = b"aw2246french44pledgeor"
setting  = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$"
target   = b"$y$j9T$F/vLDJRdzzspQonYxyqKl1$Q/nOKF5ECoPwQIJAZSlNcRt21Y3b1eV42Usj5SkfBX9"

got = lib.crypt(password, setting)
print(got)
print("MATCH" if got == target else "NO MATCH")
