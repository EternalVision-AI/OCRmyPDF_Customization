#!/usr/bin/env python3

license = """OCRmyPDF Essentials

Make your PDF files text-searchable (A GUI for OCRmyPDF)

Copyright (C) 2021 Björn Seipel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see 

"""

from os import path, environ, getcwd, makedirs, listdir, remove, set_blocking 
import PySimpleGUI_4_60 as sg
import sys, ast, signal, subprocess, shlex
import queue
import glob
from copy import deepcopy
from configparser import ConfigParser, NoOptionError
from random import randint
from tempfile import TemporaryDirectory, tempdir
from shutil import copytree
import logging
import argparse
import darkdetect
import uuid


iconstring=b'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'

parser = argparse.ArgumentParser(description="OCR and QR / Barcode based splitter for PDF files")

parser.add_argument('--log', default="WARNING", choices=['WARNING', 'INFO', 'DEBUG'],
                    help='Available log levels: WARNING, INFO, DEBUG')

args = parser.parse_args()

log = logging.getLogger('OCRmyPDF')
loglevel=logging.getLevelName(args.log)
if isinstance(loglevel, int):
    logging.basicConfig(level=loglevel)
else:
    raise ValueError('Invalid log level: %s' % loglevel)

if darkdetect.isDark():
    log.info('Dark mode detected. Using dark theme.')
    themedef = {
    'BACKGROUND': '#272727', 
    'TEXT': '#CCCCCC', 
    'INPUT': '#222222', 
    'TEXT_INPUT': '#CCCCCC', 
    'SCROLL': '#4A4A4A',
    'BUTTON': ('#CCCCCC', '#373737'), 
    'PROGRESS': ('#E95420', '#4A4A4A'), 
    'BORDER': 1, 
    'SLIDER_DEPTH': 0, 
    'PROGRESS_DEPTH': 0,
    'COLOR_LIST': ['#CCCCCC', '#2A2A2A', '#E95420', '#272727'], 
    'DESCRIPTION': ['Grey', 'White', 'Orange'] }
    
    # Colors not taken from theme:
    readonly_background_color = '#222222'
    readonly_text_color       = '#CCCCCC'
    highlight_bg_color        = '#E95420'
    highlight_t_color         = 'white'

    sg.theme_add_new ('MimicJammyJellyfishDark', themedef)

    theme='MimicJammyJellyfishDark'
else:    
    log.info('Light mode detected. Using light theme.')
    theme='DefaultNoMoreNagging'

    # Colors not taken from theme:
    readonly_background_color = None
    readonly_text_color       = None
    highlight_bg_color        = 'green'
    highlight_t_color         = 'white'

sg.theme(theme)   

#App values
aboutPage = 'https://github.com/digidigital/OCRthyPDF-Essentials/blob/main/About.md'
version = '1.0'
applicationTitle = 'AdamPDF Essentials'

# Read licenses
license += """
********************************************
The following components are libraries used by this program 
or distributed as dependencies in a Snap or AppImage
********************************************
"""
licensePath = path.abspath(path.dirname(__file__))+ '/../licenses'
licenses = listdir(licensePath)
for f in licenses:
    license += "\n\n#*#*#*#*# " + f.split("_", 1)[0] + " #*#*#*#*#\n\n"
    with open(licensePath + '/' + f) as licenseFile:
        license += licenseFile.read()

# Config related
# 'background', temporarilyy diabled since ocrmypdf v13.0.0
stringOptions = ['ocr', 'noise', 'optimization', 'postfix', 'standard', 'confidence','userwordsfilename', 
                 'deskew', 'rotate', 'sidecar', 'runsplitter', 'tess-thresholding', 'savesplittext',
                 'separator', 'separatorpage', 'usesourcename', 'loglevel', 'areafactor']

pathOptions = ['filename','infolder','outfolder']

configPath = environ['HOME']+'/.config/OCRthyPDF'
configini = configPath + '/config_0_6_2.ini'
config = ConfigParser()

try:
    user_home = environ['SNAP_REAL_HOME']
except KeyError:
    user_home = environ['HOME']

# Other
runningOCR = False
runningSPLIT = False
splitJobs = queue.Queue()
ocrJobs = queue.Queue()
Job={'running': False}
tmpdir = TemporaryDirectory()

log.debug('Temporary directory: ' + tmpdir.name)

# Needed for pyinstaller onefile...
try:
    scriptRoot = sys._MEIPASS
except Exception:
    scriptRoot = path.dirname(path.realpath(__file__))
    
#set the script root if in Snap environment
if "SNAP_COMMON" in environ:
    scriptRoot = environ['SNAP'] + '/code'

# OCRmyPDF Exit codes
exitCode = { 
    0 : 'Returncode 0. Job completed.',
    1 : 'Invalid arguments, exited with an error.',
    2 : 'The input file does not seem to be a valid PDF.',
    3 : 'An external program required by OCRmyPDF is missing.',
    4 : 'An output file was created, but it does not seem to be a valid PDF. The file will be available.',
    5 : 'The user running OCRmyPDF does not have sufficient permissions to read the input file and write the output file. Maybe you need to adjust the settings in the Snap store',
    6 : 'The file already appears to contain text so it may not need OCR. See output message.',
    7 : 'An error occurred in an external program (child process) and OCRmyPDF cannot continue.',
    8 : 'The input PDF is encrypted. OCRmyPDF does not read encrypted PDFs. Use another program such as AESify to remove encryption.',
    9 : 'A custom configuration file was forwarded to Tesseract using --tesseract-config, and Tesseract rejected this file.',
    10 : 'A valid PDF was created, PDF/A conversion failed. The file will be available.',
    15 : 'Some totally unexpexted error occurred.',
    130 : 'The program was interrupted by pressing Stop OCR button.'
}

queuePercent = lambda a, b : int(a/b*100)

def getLangs():
    log.info('Checking for installed tesseract languages.')
    # tesseractOutput = subprocess.check_output('tesseract --list-langs', stderr=subprocess.STDOUT , shell=True, text=True).split('\n')
    # seems not work in snap's standard core18 python version.
    # Keeping it for future revision since workaround seems easier than adding required version of python to snap ;)
    args = shlex.split('tesseract --list-langs')
    p = subprocess.Popen (args,stdout=subprocess.PIPE)
    tesseractOutput = []
    while True:
        tesseractOutput.append(p.stdout.readline().decode().strip())
        if p.poll() is not None:
            break  
    log.debug(tesseractOutput)
    languageList = []
    for line in tesseractOutput:
        if line != 'osd' and line != '' and not line.startswith('List'):
            languageList.append(line)
    languageList.sort()
    return languageList         

def readConfig():
    log.debug('Reading config')
    config.read(configini)
    window['opt_languages'].set_value(ast.literal_eval(config.get('Languages', 'opt_languages')))       
    for option in pathOptions:
        newPath = config.get('OCRthyPDFpaths', option)
        window[option].update(value = newPath)
        window[option + '_short'].update(value = limitFilenameLen(newPath))
        # Enable Start button
        if option != '' and option in ('filename', 'infolder'):
            window['start_ocr'].update(disabled=False) 
    for o in stringOptions:
        try:
            window['opt_' + o].update(value = config.get('OCRmyPDFoptions', 'opt_' + o))
        except NoOptionError:
            logging.debug('No config option for ' + o)    
          
def writeConfig():
    log.debug('Creating / Updating config')
    event, values = window.read(timeout = 0) 
    config.set('Languages', 'opt_languages' , repr(values['opt_languages']))
    for option in stringOptions:
        config.set('OCRmyPDFoptions', 'opt_' + option, str(values['opt_' + option]))
    for option in pathOptions:
        config.set('OCRthyPDFpaths', option, str(values[option]))    
    with open(configini, 'w+') as configfile:
        config.write(configfile)

def updateInitialFolders():
    if window['outfolder'].get() != '':
        window['outfolder_browse'].InitialFolder = window['outfolder'].get()
    else:
        window['outfolder_browse'].InitialFolder = user_home
    if window['infolder'].get() != '':
        window['infolder_browse'].InitialFolder = window['infolder'].get()
    else:
        window['infolder_browse'].InitialFolder = user_home
    if window['filename'].get() != '':
        window['file_browse'].InitialFolder = path.dirname(window['filename'].get()) 
    else:
        window['file_browse'].InitialFolder = user_home
        
# Just a simple popup message in a function so I can change formatting and behaviour in one place. :)
def popUp(message):
    windowLocation = window.current_location()
    popWindow = sg.Window('',
        [[sg.Text(message)],
        [sg.OK()]
        ], 
        element_justification = 'c',
        no_titlebar = True,
        font=('FreeSans', 11, 'normal'),
        auto_close= True,
        auto_close_duration = 10,
        modal=True,
        finalize = True, 
        keep_on_top = True,
        location = (windowLocation[0]+window.size[0]/3,windowLocation[1]+window.size[1]/3)       
    )
        
    while True:
        event, values = popWindow.read() 
        if event == sg.WIN_CLOSED: 
            break
        else:
            popWindow.close()

# If filename is longer than 'limit' split filename in two shorter parts an add '...' in the middle so it fits in limit
def limitFilenameLen(filename, limit=57):
    x = len(filename)
    if x <= limit:
        return filename
    else:
        return filename[0:int(limit/2 - 3)] + '...' + filename[x - int(limit/2 - 3):x]  


def toggleButtons():
    #start button
    if window['start_ocr'].Disabled: 
        window['start_ocr'].update(disabled=False)
    else:
        window['start_ocr'].update(disabled=True)
    #stop button
    if window['stop_ocr'].Disabled:
        window['stop_ocr'].update(disabled=False)
    else:
        window['stop_ocr'].update(disabled=True)


def deleteFiles(folder):
    for file in listdir(folder):
        remove(path.join(folder, file))


def cleanup(Job, popup=True):
    #empty queues 
    while splitJobs.qsize()>0:
        splitJobs.get()
    while ocrJobs.qsize()>0:
        ocrJobs.get()

    Job['ocrQueueLen']=0
    Job['splitQueueLen']=0 
    
    #enable buttons
    toggleButtons()

    #reset Job
    Job['file']=''
    Job['type']=''
    Job['running']=False
    Job['process']=''

    if popup:
        popUp("All jobs completed")

    #Reset queue bars in case jobs were stopped by user
    window['ocr_queue_bar'].update(0)
  
    log.info('Cleanup complete.')
    return Job

def startSplitJob (filename, Job):
    Job['file']=filename
    Job['progressValue']=0
    Job['type']='split'
    
    args=''

    # Separator
    args = args + "-s '" + tmpOptions['opt_separator'] + "' "
  
    # Sticker Mode
    if tmpOptions['opt_separatorpage'] == 'Sticker Mode':
        args = args + '--sticker-mode '

    # DEPRECATED: Assemble split parts from repaired PDF
    '''
    if tmpOptions['opt_repair'] == 'yes':
        args = args + '-r '    
    '''
    
    args = args + '--tesseract-timeout 600' + ' '
    args = args + '--tesseract-downsample-large-images' + ' '
    args = args + '--tesseract-downsample-above 5000' + ' '
    args = args + '--invalidate-digital-signatures' + ' '


    args = args + '-af ' + tmpOptions['opt_areafactor'] + ' '
    
    # Loglevel
    args = args + "--log " + tmpOptions['opt_loglevel'] + " "
    
    # Drop filename
    if tmpOptions['opt_usesourcename'] == 'no':
        args = args + '-d ' 
    
    # Save txt files
    if tmpOptions['opt_savesplittext'] == 'yes':
        args = args + '-t '   
    
    #  Output folder
    args = args + " -o '" + tmpdir.name + "'"
  
    commandLine = "'" + scriptRoot + "/splitter.py' '" + Job['file'] + "' " + args
    log.debug('Commandline: ' + commandLine)
    execute = shlex.split(commandLine)
        
    Job['process'] = subprocess.Popen (execute,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #make STDOUT/readline non-blocking!
    set_blocking(Job['process'].stdout.fileno(), False)
    
    Job['running']=True

    log.info('Split job started: ' + Job['file'])
    
    if window['tmp_log'].get() == 'yes': 
        window['console'].update(value=commandLine + "\n")
    else:
        window['console'].print(commandLine)
    
    return Job

def startOCRJob (filename, Job):
    Job['file']=filename
    Job['progressValue']=0
    Job['type']='ocr'
        
    args=''

    # Verbose output
    if tmpOptions['opt_loglevel'] == 'DEBUG':
        args = args + "-v "
    # OCR languages
    for l in tmpOptions['opt_languages']:
        args = args + "-l " + l + " "

    # ocr PDF Renderer hocr sandwich
    ocrRenderer = tmpOptions['opt_renderer']
    if ocrRenderer == "hocr":
        args=args + "--pdf-renderer hocr "
    elif ocrRenderer == "sandwich":
        args=args + "--pdf-renderer sandwich "
    
    # ocr use multiple cores
    ocrJobs = tmpOptions['opt_jobs']
    args = args + '--jobs '+ ocrJobs + ' '

    # ocr PDF page segmentation mode
    ocrPsm = tmpOptions['opt_psm']
    psmArr = ['Orientation and script detection (OSD) only', 'Automatic page segmentation with OSD', 'Automatic page segmentation, but no OSD', 'Fully automatic page segmentation, but no OSD (default)', 'Assume a single column of text of variable sizes', 'Assume a single uniform block of vertically aligned text', 'Assume a single uniform block of text', 'Treat the image as a single text line', 'Treat the image as a single word', 'Treat the image as a single character', 'Block segmentation, but no text line or word segmentation']
    # for index, opt in enumerate(psmArr):
    #     if ocrPsm == opt:
    #         args=args + "--tessedit_pageseg_mode " + str(index) + " "
    args=args + "--tesseract-config tesseract_config.txt "

    # ocr strategy --redo-ocr --force-ocr
    ocrStrat = tmpOptions['opt_ocr']
    if ocrStrat == "Redo OCR":
        args=args + "--redo-ocr "
    elif ocrStrat == "Force OCR":
        args=args + "--force-ocr "
    else:
        args=args + "--skip-text "     
    # clean
    clean = tmpOptions['opt_noise']
    if clean == "Clean for OCR but keep original page":
        args=args + "--clean "
    elif clean == "Clean for OCR and keep cleaned page":
        args=args + "--clean-final "

    # sidecar
    if tmpOptions['opt_sidecar'] == 'yes':
        args = args + "--sidecar "

    # background (Temporarily disabled since ocrmypdf v13.0.0)
    '''
    if tmpOptions['opt_background'] == 'yes':
        args = args + "--remove-background "    
    '''
    # tesseract user words
    if len(tmpOptions['opt_userwordsfilename'])>0:
         args=args + '--user-words "%s" ' % tmpOptions['opt_userwordsfilename']

    # tesseract thresholding
    tessThresholding = tmpOptions['opt_tess-thresholding']
    if tessThresholding == "adaptive-otsu":
        args=args + "--tesseract-thresholding adaptive-otsu "
    elif tessThresholding == "sauvola":
        args=args + "--tesseract-thresholding sauvola "
    else:
        args=args + "--tesseract-thresholding otsu "
    
    # deskew
    if tmpOptions['opt_deskew'] == 'yes':
        args = args + "--deskew "

    # rotate pages
    if tmpOptions['opt_rotate'] == 'yes':
        args = args + "--rotate-pages --rotate-pages-threshold " + str(tmpOptions['opt_confidence']) + " "

    # optimization
    args=args + "--optimize " + str(tmpOptions['opt_optimization']) + " "

    # output type
    args=args + "--output-type "
    outputType = tmpOptions['opt_standard']
    if outputType == "PDF/A-1b":
        args=args + "pdfa-1 "
    elif outputType == "PDF/A-2b":
        args=args + "pdfa-2 "
    elif outputType == "PDF/A-3b":
        args=args + "pdfa-3 "
    else: 
        args=args + "pdf "
    
    # print(args)
    inputFilename = path.basename(Job['file'])
    outFileParts = inputFilename.rsplit('.', 1)
    outFile = path.join(tmpOptions['outfolder'], outFileParts[0] + tmpOptions['opt_postfix'] + '.' + outFileParts[1])
    Job['outfile'] = outFile 
    commandLine = "ocrmypdf --use-threads " + args + "'" + Job['file'] + "' '" + outFile + "'"

    execute = shlex.split(commandLine)
    log.debug('Commandline: ' + commandLine)
    Job['process'] = subprocess.Popen (execute,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #make STDOUT/readline non-blocking!
    set_blocking(Job['process'].stdout.fileno(), False)
    
    Job['running']=True
    log.info('OCR job started' + Job['file'])
    
    if window['tmp_log'].get() == 'yes': 
        window['console'].update(value=commandLine + "\n")
    else:
        window['console'].print(commandLine)
    
    return Job

# checks the queues according to their priority and starts the next job
def nextJob(previousJob=None):
    
    # delete ocr'ed file if a split job ran  
    if previousJob and previousJob['type'] == 'split':
        remove(previousJob['file'])
        copytree (tmpdir.name , tmpOptions['outfolder'], dirs_exist_ok=True)
        deleteFiles(tmpdir.name)
        
    # check if we have to run a split job after ocr
    if previousJob and previousJob['type'] == 'ocr':
        if tmpOptions['opt_runsplitter'] == 'yes':
            splitJobs.put(previousJob['outfile'])
                      
    if not previousJob:
        log.info('Creating first job.')
        previousJob={'running': False, 'ocrQueueLen' : 0, 'splitQueueLen' : 0}
    
    if ocrJobs.qsize() > previousJob['ocrQueueLen']:
        previousJob['ocrQueueLen'] = ocrJobs.qsize()
    if splitJobs.qsize() > previousJob['splitQueueLen']:
        previousJob['splitQueueLen'] = splitJobs.qsize()   

    log.debug('Checking queues for next job. OCR-queue: ' + str(ocrJobs.qsize()) + ', Split-queue:' + str(splitJobs.qsize()))

    if splitJobs.qsize() > 0:      
        Job = startSplitJob (splitJobs.get(), previousJob)

    elif ocrJobs.qsize() > 0:
        Job = startOCRJob (ocrJobs.get(), previousJob) 
        window['ocr_queue_bar'].update(queuePercent(ocrJobs.qsize(), previousJob['ocrQueueLen']))

    else:
        Job = cleanup(previousJob)
        
    return Job

# Language related
languages = getLangs()
languageCodes = { 
    'aa':'aar', 'ab':'abk', 'ae':'ave', 'af':'afr', 'ak':'aka', 'am':'amh', 'an':'arg', 'ar':'ara', 'as':'asm', 'av':'ava', 
    'ay':'aym', 'az':'aze', 'ba':'bak', 'be':'bel', 'bg':'bul', 'bh':'bih', 'bi':'bis', 'bm':'bam', 'bn':'ben', 'bo':'bod', 
    'br':'bre', 'bs':'bos', 'ca':'cat', 'ce':'che', 'ch':'cha', 'co':'cos', 'cr':'cre', 'cs':'ces', 'cu':'chu', 'cv':'chv', 
    'cy':'cym', 'da':'dan', 'de':'deu', 'dv':'div', 'dz':'dzo', 'ee':'ewe', 'el':'ell', 'en':'eng', 'eo':'epo', 'es':'spa', 
    'et':'est', 'eu':'eus', 'fa':'fas', 'ff':'ful', 'fi':'fin', 'fj':'fij', 'fo':'fao', 'fr':'fra', 'fy':'fry', 'ga':'gle', 
    'gd':'gla', 'gl':'glg', 'gn':'grn', 'gu':'guj', 'gv':'glv', 'ha':'hau', 'he':'heb', 'hi':'hin', 'ho':'hmo', 'hr':'hrv', 
    'ht':'hat', 'hu':'hun', 'hy':'hye', 'hz':'her', 'ia':'ina', 'id':'ind', 'ie':'ile', 'ig':'ibo', 'ii':'iii', 'ik':'ipk', 
    'io':'ido', 'is':'isl', 'it':'ita', 'iu':'iku', 'ja':'jpn', 'jv':'jav', 'ka':'kat', 'kg':'kon', 'ki':'kik', 'kj':'kua', 
    'kk':'kaz', 'kl':'kal', 'km':'khm', 'kn':'kan', 'ko':'kor', 'kr':'kau', 'ks':'kas', 'ku':'kur', 'kv':'kom', 'kw':'cor', 
    'ky':'kir', 'la':'lat', 'lb':'ltz', 'lg':'lug', 'li':'lim', 'ln':'lin', 'lo':'lao', 'lt':'lit', 'lu':'lub', 'lv':'lav', 
    'mg':'mlg', 'mh':'mah', 'mi':'mri', 'mk':'mkd', 'ml':'mal', 'mn':'mon', 'mr':'mar', 'ms':'msa', 'mt':'mlt', 'my':'mya', 
    'na':'nau', 'nb':'nob', 'nd':'nde', 'ne':'nep', 'ng':'ndo', 'nl':'nld', 'nn':'nno', 'no':'nor', 'nr':'nbl', 'nv':'nav', 
    'ny':'nya', 'oc':'oci', 'oj':'oji', 'om':'orm', 'or':'ori', 'os':'oss', 'pa':'pan', 'pi':'pli', 'pl':'pol', 'ps':'pus', 
    'pt':'por', 'qu':'que', 'rm':'roh', 'rn':'run', 'ro':'ron', 'ru':'rus', 'rw':'kin', 'sa':'san', 'sc':'srd', 'sd':'snd', 
    'se':'sme', 'sg':'sag', 'si':'sin', 'sk':'slk', 'sl':'slv', 'sm':'smo', 'sn':'sna', 'so':'som', 'sq':'sqi', 'sr':'srp', 
    'ss':'ssw', 'st':'sot', 'su':'sun', 'sv':'swe', 'sw':'swa', 'ta':'tam', 'te':'tel', 'tg':'tgk', 'th':'tha', 'ti':'tir', 
    'tk':'tuk', 'tl':'tgl', 'tn':'tsn', 'to':'ton', 'tr':'tur', 'ts':'tso', 'tt':'tat', 'tw':'twi', 'ty':'tah', 'ug':'uig', 
    'uk':'ukr', 'ur':'urd', 'uz':'uzb', 've':'ven', 'vi':'vie', 'vo':'vol', 'wa':'wln', 'wo':'wol', 'xh':'xho', 'yi':'yid', 
    'yo':'yor', 'za':'zha', 'zh':'zho', 'zu':'zul'
}
systemLanguage = environ['LANG'][0:2]
log.debug('System language identified as: ' + systemLanguage)

tab1_layout =   [
                    [sg.T('PDF Renderer:'), sg.InputCombo(('hocr', 'sandwich'), default_value='sandwich', key='opt_renderer', enable_events = True)],  
                    [sg.T('Use Multiple Cores:'), sg.InputCombo(('1', '2', '3', '4'), default_value='1', key='opt_jobs', enable_events = True)],  
                    [sg.T('Page Segamentation Mode:'), sg.InputCombo(('Orientation and script detection (OSD) only', 'Automatic page segmentation with OSD', 'Automatic page segmentation, but no OSD', 'Fully automatic page segmentation, but no OSD (default)', 'Assume a single column of text of variable sizes', 'Assume a single uniform block of vertically aligned text', 'Assume a single uniform block of text', 'Treat the image as a single text line', 'Treat the image as a single word', 'Treat the image as a single character', 'Block segmentation, but no text line or word segmentation'), default_value='Assume a single column of text of variable sizes', key='opt_psm', enable_events = True)],  
                    [sg.T('Existing text/OCR strategy:'), sg.InputCombo(('Skip pages with text', 'Redo OCR', 'Force OCR'), default_value='Force OCR', key='opt_ocr', enable_events = True)],  
                    [sg.T('Deskew pages (crooked scans):', tooltip = 'Will correct pages scanned at a skewed angle by rotating them back into place.'),sg.InputCombo(('yes', 'no'), default_value='yes', key='opt_deskew', enable_events = True, tooltip = 'Will correct pages scanned at a skewed angle by rotating them back into place.')],
                    [sg.T('Fix page rotation:', tooltip = 'Attempts to determine the correct orientation for each page and rotates the page if necessary.'),sg.InputCombo(('yes', 'no'), default_value='yes', key='opt_rotate', enable_events = True, tooltip = 'Attempts to determine the correct orientation for each page and rotates the page if necessary.')],
                    [sg.T('Minimum page rotation confidence:'),sg.Spin(('5','10', '15', '20', '25'),initial_value = '5', key='opt_confidence', size=(2,1),enable_events=True, tooltip = 'Adjust this value if you are getting too many false positives for page rotation.')],
                    [sg.T('Noise:'), sg.InputCombo(('Do nothing', 'Clean for OCR but keep original page', 'Clean for OCR and keep cleaned page'), default_value='Clean for OCR but keep original page', key='opt_noise', enable_events = True, tooltip = 'Clean up pages before OCR. If you keep the cleaned pages review the OCRed PDF!')],
                    # Tempoarily disabled since ocrmydf v13.0.0
                    #  [sg.T('Remove background:'), sg.InputCombo(('yes', 'no'), default_value='no', key='opt_background', enable_events = True), visible=False],
                    [sg.T('Optimization level:'), sg.InputCombo(('0', '1', '2', '3'), default_value='3', key='opt_optimization', enable_events = True, tooltip = '0 = Disables optimization, 1 = Lossless optimizations, 2 + 3 = Reduced image quality ')],
                    [sg.T('Tesseract thresholding:'), sg.InputCombo(('otsu', 'adaptive-otsu', 'sauvola'), default_value='sauvola', key='opt_tess-thresholding', enable_events = True, tooltip = 'Adjust to improve OCR accuracy. Best setting depends on the scanned document\n(e.g. shadow artefacts, background colors, light or dark text). Default is otsu.\nTesseract 5.0.0+ only.')],
                    [sg.T('Output type:'), sg.InputCombo(('Standard PDF', 'PDF/A-1b', 'PDF/A-2b', 'PDF/A-3b'), default_value='PDF/A-2b', key='opt_standard', enable_events = True)],
                    [sg.T('Postfix (may overwrite original if empty!):'), sg.In('_OCR', key='opt_postfix', change_submits = True, size = (15,1), enable_events = True)],
                    [sg.T('Save recognized text as separate .txt file:'),sg.InputCombo(('yes', 'no'), default_value='no', key='opt_sidecar', enable_events = True)]          
                ]   

tab2_layout =   [
                    [sg.T('Separator pattern for QR Code (postfix is optional): <Separator_Code>|<Custom_Postfix>')],
                    [sg.T('<Custom_Postfix> is added to the filename in "Sticker Mode" if available')],
                    [sg.T('It replaces the index numbers -> You need to provide different postfixes for all files.')],
                    [sg.T('Run splitter after OCR:'),sg.InputCombo(('yes', 'no'), default_value='no', key='opt_runsplitter', enable_events = True)],
                    [sg.T('Separator code (add at least this to your QR code):'), sg.In('NEXT', key='opt_separator', change_submits = True, size = (15,1), enable_events = True)],
                    [sg.T('Separator mode?:'), sg.InputCombo(('Drop separator page', 'Sticker Mode'), default_value='Drop separator page', key='opt_separatorpage', tooltip='Sticker Mode: QR Code starts new segment. Page is added to output.', enable_events = True)],                  
                    [sg.T('Use source filename in output filename?:'),sg.InputCombo(('yes', 'no'), default_value='yes', key='opt_usesourcename', enable_events = True)],
                    [sg.T('Limit QR-code search area:'),sg.InputCombo(('1.0','0.5','0.25'), default_value='1', key='opt_areafactor', tooltip='Default: 1.0 - Multiply width and height with this factor to\nlimit the search area and speed up splitting.\n1 = Whole image(page)\n0.5 = Upper left quadrant\n0.25 = Upper left quadrant of upper left quadrant', enable_events = True)],
                    [sg.T('Save text as separate .txt files:'),sg.InputCombo(('yes', 'no'), default_value='no', key='opt_savesplittext', enable_events = True)]                        
                ]                   

tab3_col1 =   [
                    [
                        sg.T('Select document language(s):')
                    ],
                    [ 
                        sg.Listbox(values=languages, key='opt_languages', select_mode='multiple', highlight_background_color = highlight_bg_color, highlight_text_color = highlight_t_color, enable_events = True, expand_x=True, expand_y =True)# xsize=(15, 12))
                    ]
                ]   

tab3_col2 =   [
                    [
                        sg.T('Advanced language options')
                    ],
                    [
                        sg.Text('''Specify the location of a Tesseract user words text file.
This is a list of words (one word in each line) Tesseract
should consider while performing OCR in addition to its 
standard language dictionaries. This can improve OCR
quality especially for specialized and technical documents.''')
                    ],
                    [ 
                        sg.InputText(key='opt_userwordsfilename', size=(28), visible=True, readonly=True, disabled_readonly_background_color = readonly_background_color, disabled_readonly_text_color = readonly_text_color, enable_events=True), 
                        sg.FileBrowse(('Browse'), key='userwordfile_browse',initial_folder=user_home),
                        sg.Button(('Reset'), key='reset_userfile')
                    ]

                ]  

tab3_layout =   [
                    [            
                        sg.Column(tab3_col1, expand_y=True, vertical_alignment = 't'), 
                        sg.Column(tab3_col2, vertical_alignment = 't')      
                    ]
                ]  

colQueue1 = [
                [
                    sg.Text('OCR Job Queue: ', pad = ((0,0),(4,0))) 
                ]
            ]   

colQueue2 = [
                [
                    sg.ProgressBar(100, key='ocr_queue_bar', size=(44,20))  
                ]
            ]

tab4_layout =   [
                    [
                        sg.Multiline('', key='console', expand_x = True, expand_y = True)
                    ],
                    [
                        sg.T('Loglevel:'), sg.InputCombo(('INFO', 'DEBUG'), default_value='INFO', key='opt_loglevel', enable_events = True),
                        sg.T('Limit console to display last job only?:'),sg.InputCombo(('yes', 'no'), default_value='yes', key='tmp_log', enable_events = True),
                    
                    ],
                    [            
                        sg.Column(colQueue1, vertical_alignment = 't'), sg.Column(colQueue2)      
                    ]
                ] 

tab5_layout =   [
                    [
                        sg.Multiline(license, expand_x = True, expand_y = True)
                    ]
                ] 

col1 =  [
            [
                sg.Text('Single PDF:', pad = ((5,0),(8,0)))
            ],
            [
                sg.Text('Input Folder:', pad = ((5,0),(16,0))) 
            ],
            [
                sg.Text('Output Folder:', pad = ((5,0),(16,0)))
            ]
        ]   
col2 =  [
            [
                sg.InputText(key='filename_short', disabled_readonly_background_color = readonly_background_color, disabled_readonly_text_color = readonly_text_color,  readonly=True, size=(52,1)), 
                sg.InputText(key='filename', visible=False, readonly=True, enable_events=True), 
                sg.FileBrowse(('Browse'), key='file_browse', file_types=(("PDF", "*.pdf"),("PDF", "*.PDF")), initial_folder=user_home)
            ],
            [
                sg.InputText(key='infolder_short', disabled_readonly_background_color = readonly_background_color, disabled_readonly_text_color = readonly_text_color, readonly=True, size=(52,1)), 
                sg.InputText(key='infolder', visible=False,  readonly=True, enable_events=True), 
                sg.FolderBrowse(('Browse'), key='infolder_browse', initial_folder=user_home)
            ],
            [
                sg.InputText(key='outfolder_short', disabled_readonly_background_color = readonly_background_color, disabled_readonly_text_color = readonly_text_color, readonly=True, size=(52,1)), 
                sg.InputText(key='outfolder', visible=False,  readonly=True, enable_events=True), 
                sg.FolderBrowse(('Browse'), key='outfolder_browse', initial_folder=user_home)
            ]
        ]


layout = [  
            [
                sg.Column(col1, vertical_alignment = 't'), sg.Column(col2)      
            ],
            
            [
                sg.TabGroup([[
                    sg.Tab('OCR', tab1_layout), 
                    sg.Tab('Splitter', tab2_layout),
                    sg.Tab('Languages', tab3_layout),
                    sg.Tab('Console', tab4_layout),
                    sg.Tab('Licenses', tab5_layout)
                ]], size = (None,None))
            ], 
            [
                sg.Button('Start OCR', key='start_ocr', disabled = True),
                sg.Button('Stop OCR', key='stop_ocr', disabled = True),
                sg.ProgressBar(100, key='progress_bar', size=(39,20))  
            ]
         ]

# Create the Window

window = sg.Window(applicationTitle  + ' ' + version, layout, icon=iconstring , font=('FreeSans', 11, 'normal'), finalize = True)

# Check if config file exists and create one if none exists 

if len(config.read(configini)) == 0:
    makedirs(configPath, exist_ok=True)
    config.add_section('App')
    config.set('App', 'version', version)
    config.add_section('Languages')
    config.add_section('OCRmyPDFoptions')
    config.add_section('OCRthyPDFpaths')

    # Check if system language is available for OCR and set it as additional default
    if systemLanguage in languageCodes: 
        if languageCodes[systemLanguage] in languages:
            window['opt_languages'].set_value(['eng', languageCodes[systemLanguage]])
    
    event, values = window.read(timeout=0)

    writeConfig()
else:
    readConfig()  

updateInitialFolders()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    if Job['running']==True:
        line = Job['process'].stdout.readline().decode()
        
        #update console tab
        if line != '':
            window['console'].print(line)
            
            Job['progressValue'] += 5
        else:
            #fake some output for long running steps :)
            Job['progressValue'] += 1 #randint(0,5)

        # Animate progress bar
        if Job['progressValue'] > 100:
            Job['progressValue'] = 0
        window['progress_bar'].update(Job['progressValue'])
        if event == 'stop_ocr':
            window['console'].print('"Stop OCR" requested')

            #Try to stop subprocess with SIGINT - if timeout occurs kill it
            try: 
                Job['process'].send_signal(signal.SIGINT)
                Job['process'].wait(timeout=10)
                window['console'].print('Process was stopped with SIGINT')
            except subprocess.TimeoutExpired:
                Job['process'].kill()
                Job['process'].wait(timeout=10)
                window['console'].print('Process was killed')
                             
        if Job['process'].poll() is not None: 
            
            if Job['process'].returncode in (0, 10):
                exitMessage = exitCode[Job['process'].returncode]
                log.debug('Job Exit-Code: ' + exitMessage)
                #reset progress bar
                window['progress_bar'].update(0)
            
                Job = nextJob(Job)

            elif Job['process'].returncode in (1,2,3,4,5,6,7,8,9,15,130):
                exitMessage = exitCode[Job['process'].returncode]  
                log.debug('Job Exit-Code: ' + exitMessage)
                #debug
                while True:
                    line = Job['process'].stdout.readline().decode()
                    #update console tab
                    if line != '':
                        window['console'].print(line)
                    else:
                        break
                popUp(exitMessage)
                Job = cleanup(Job, popup=False)    
            else:
                exitMessage = "Process stopped with return code %d\nThis can happen when a subprocess is running.\nNothing to worry about if you have pressed the 'Stop OCR' button."%(Job['process'].returncode)  
                #debug
                while True:
                    line = Job['process'].stdout.readline().decode()
                    #update console tab
                    if line != '':
                        window['console'].print(line)
                    else:
                        break
                popUp(exitMessage)
                Job = cleanup(Job, popup=False)

            window['console'].print(exitMessage)
            #reset progress bar
            window['progress_bar'].update(0)

        event, values = window.read(timeout = 10)    
    else:
        event, values = window.read() 
    
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break   

    # Enable Start button
    if Job['running'] == False and (values['filename'] != '' or values['outfolder'] != ''):
        window['start_ocr'].update(disabled=False) 
    # Disable start button if no input selected 
    if values['filename'] == '' and values['outfolder'] == '':
        window['start_ocr'].update(disabled=True)     

    if event == 'filename' and not values['filename'] == '' : 
        # Shorten filename so it fits in the input text field
        window['filename_short'].update(value = limitFilenameLen(values['filename'])) 
        # Clear infolder
        window['infolder'].update(value = '')
        window['infolder_short'].update(value = '')
        # If outfolder is empty set to same folder as input folder
        if values['outfolder'] == '':
            inFilePath = path.dirname(values['filename'])
            window['outfolder'].update(value = inFilePath)
            window['outfolder_short'].update(value = limitFilenameLen(inFilePath))
        updateInitialFolders()

    if event =='reset_userfile':
        window['opt_userwordsfilename'].update(value='')

    if event == 'infolder' and not values['infolder'] == '' : 
        inFolderPath = values['infolder']
        # Shorten filename so it fits in the input text field
        window['infolder_short'].update(value = limitFilenameLen( inFolderPath)) 
        # Clear single PDF input
        window['filename'].update(value = '')
        window['filename_short'].update(value = '')
        # If outfolder is empty set to same folder
        if values['outfolder'] == '':
            window['outfolder'].update(value =  inFolderPath)
            window['outfolder_short'].update(value = limitFilenameLen( inFolderPath))
        updateInitialFolders()

    if event == 'outfolder' and not values['outfolder'] == '' : 
        # Shorten filename so it fits in the input text field
        window['outfolder_short'].update(value = limitFilenameLen(values['outfolder'])) 
        updateInitialFolders()
       
    if event.startswith('opt_') or event in pathOptions:
        writeConfig()
      
    if event == 'start_ocr':
        log.info('OCR queue started')
        fileList=[]
        
        if values['filename'] != '':
            fileList.append(values['filename'])
        else:
            for file in glob.glob(values['infolder'] + '/*.pdf'):
                fileList.append(file)
            for file in glob.glob(values['infolder'] + '/*.PDF'):
                fileList.append(file)
        
        for file in fileList:
            ocrJobs.put(file) 
        

        #copy values into temporary object to prevent user from changing
        #options of already running jobs 
        tmpOptions = deepcopy(values)

        toggleButtons()

        # get the first job 
        Job = nextJob()   
