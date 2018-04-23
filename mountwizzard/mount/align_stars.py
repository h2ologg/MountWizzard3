############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.4
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
###########################################################
import logging
import PyQt5
import time
import copy
import operator
import numpy


class AlignStars:
    logger = logging.getLogger(__name__)

    # alignment stars of 10micron with (ra(deg), dec(deg))
    star = dict()
    star['Albireo'] = [292.68033548, 27.95968007]
    star['Aldebaran'] = [68.98016279, 16.50930235]
    star['Alderamin'] = [319.6448847, 62.58557446]
    star['Algenib'] = [3.30896346, 15.18359354]
    star['Alkaid'] = [206.88515734, 49.31326673]
    star['Alpha Cam'] = [73.51254332, 66.3426768]
    star['Alpha Fornacis'] = [48.018864, -28.98762045]
    # star['Alpha Lyrics'] = [279.23473479, 38.78368896]
    star['Alphard'] = [141.8968446, -8.65859953]
    star['Alpheratz'] = [2.09691619, 29.09043112]
    star['Altair'] = [297.6958273, 8.8683212]
    star['Alula Borealis'] = [169.61973601, 33.09430852]
    star['Antares'] = [247.35191542, -26.43200261]
    star['Arcturus'] = [213.91530029, 19.18240916]
    star['Beta Aqr'] = [322.88971548, -5.57117555]
    star['Betelgeuse'] = [88.79293899, 7.407064]
    star['Capella'] = [79.17232794, 45.99799147]
    star['Caph'] = [2.29452158, 59.1497811]
    star['Castor'] = [113.64947164, 31.88828222]
    star['Cor Caroli'] = [194.00694257, 38.31837614]
    star['Deneb'] = [310.35797975, 45.28033881]
    star['Denebola'] = [177.26490976, 14.57205806]
    star['Diphda'] = [10.89737874, -17.98660632]
    star['Dubhe'] = [165.93196467, 61.75103469]
    star['Enif'] = [326.04648391, 9.87500865]
    star['Gamma Cas'] = [14.17721542, 60.71674028]
    star['Hamal'] = [31.7933571, 23.46241755]
    star['Kochab'] = [222.6763575, 74.15550394]
    star['Lambda Aqr'] = [343.15364336, -7.57959838]
    star['Menkar'] = [45.5698878, 4.08973877]
    star['Menkent'] = [211.67061468, -36.36995474]
    star['Mirach'] = [17.43301617, 35.62055765]
    star['Mirfak'] = [51.08070872, 49.8611793]
    star['Muscida'] = [127.56612767, 60.71816987]
    star['Nu Ophiuchi'] = [254.88833333, -30.09375]
    star['Omega Cap'] = [312.95537849, -26.91912706]
    star['Pi Herculis'] = [258.76180984, 36.80916231]
    star['Polaris'] = [37.95456067, 89.26410897]
    star['Pollux'] = [116.32895777, 28.02619889]
    star['Procyon'] = [114.82549791, 5.22498756]
    star['Regulus'] = [152.09296244, 11.96720878]
    star['Rho Puppis'] = [121.88603676, -24.30432443]
    star['Rigel'] = [78.63446707, -8.20163836]
    star['Scheat'] = [345.94357275, 28.08278712]
    star['Sirius'] = [101.28715533, -16.71611586]
    star['Spica'] = [201.29824736, -11.16131949]
    star['Unukalhai'] = [236.06697631, 6.42562868]
    star['Vega'] = [279.23473479, 38.78368896]
    star['Vindemiatrix'] = [195.5441577, 10.9591504]
    star['Zaurak'] = [59.50736229, -13.50851938]
    star['Zeta Herculis'] = [250.32150433, 31.6027187]
    star['Zeta Persei'] = [58.53301032, 31.88363368]

    def __init__(self, app):
        self.app = app
