from TwainWrapper2 import Scanner

_scanner = Scanner()
_scanner.initialize_scanner()
scanner_list = _scanner.get_list_of_available_scanners()
print scanner_list
_scanner.set_scanner(scanner_list[0], 600)
_scanner.scan("C:\Users\gpatil\Desktop\misc")
