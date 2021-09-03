#!/usr/bin/python3
import sys, os, cherrypy

def derive_url(*terms, from_url=True, fragment=None):

    if from_url is True:
        from_url = cherrypy.url()
    partsIn = from_url.split('/')
    partsOut = []
    for term in terms:
        if isinstance(term, int):
            term = (term, term+1)
        if isinstance(term, tuple):
            partsOut += partsIn[slice(*term)]
        else:
            partsOut.append(term)
    derived_url = '/'.join(partsOut)
    if fragment:
        derived_url +=('#'+fragment)
    return derived_url


def main():
    prog = sys.argv.pop(0)
    print(f"let's see how I can manipulate urls using '{prog}'....")
    print(derive_url((None, -3), 'list', -2, fragment="voices_X4",
                     from_url="http://192.168.2.39:8080/abc_music/tune/view/samples/voices_X4#back"))
    #print(uo.remove(path=['view', 'samples', 'voices_X4']).add(path=('list', 'samples')))


if __name__=='__main__':
    main()
