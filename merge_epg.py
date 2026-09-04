import gzip, io, sys, urllib.request
import xml.etree.ElementTree as ET

SOURCES = [
    "https://epgshare01.online/epgshare01/epg_ripper_ES1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_MX1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_AR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CO1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CL1.xml.gz",
]

KEEP = {
    '13Rue.fr', '13emeRue.mu', '24Horas.es', '6ter.fr', '7TVRegionMurcia.es', 'AB1.fr',
    'ABXploreFR.be', 'AMC.es', 'AMITele.ca', 'APunt.es', 'ARTE.fr', 'ARTV.ca',
    'AXN.es', 'AXNMovies.es', 'Action.fr', 'AddikTV.ca', 'Animaux.fr', 'Antena3.es',
    'Antena3Internacional.es', 'AragonTV.es', 'AragonTVInt.es', 'AssembleeNationale.ca', 'Atreseries.es', 'AutoPlus.fr',
    'AztecaUno.mx', 'BBCFood.es', 'BBCHistory.es', 'BBCWorld.es', 'BFMBusiness.fr', 'BFMLyon.fr',
    'BFMMarseille.fr', 'BFMTV.fr', 'BOMCine.es', 'BabyTV.es', 'BeMad.es', 'Bloomberg.es',
    'Boing.es', 'Boomerang.fr', 'CGTNEspanol.cn', 'CGTNEspanol.es', 'CGTNFrench.cn', 'CNNInt.es',
    'CNews.fr', 'CPAC.ca', 'CStar.fr', 'Calle13.es', 'CanalCocina.es', 'CanalD.ca',
    'CanalDecasa.es', 'CanalEvasion.ca', 'CanalExtremadura.es', 'CanalExtremaduraSat.es', 'CanalHistoria.es', 'CanalPlus.fr',
    'CanalPlusBoxOffice.fr', 'CanalPlusCinema.fr', 'CanalPlusDocs.fr', 'CanalPlusFamily.mu', 'CanalPlusFoot.fr', 'CanalPlusGrandEcran.fr',
    'CanalPlusKids.fr', 'CanalPlusPremierLeague.fr', 'CanalPlusSport360.fr', 'CanalSavoir.ca', 'CanalSur.es', 'CanalSur2.es',
    'CanalSurAndalucia.es', 'CanalVie.ca', 'Canalj.fr', 'Caracol.co', 'CartoonNetwork.fr', 'Cartoonito.fr',
    'CasaTV.ca', 'CastillalaManchaTV.es', 'ChassePeche.fr', 'CinePlusClassic.fr', 'CinePlusClub.mu', 'CinePlusEmotion.fr',
    'CinePlusFestival.fr', 'CinePlusFrisson.fr', 'Cinepop.ca', 'ClanTVE.es', 'ComediePlus.mu', 'ComedyCentral.es',
    'ComedyCentral.fr', 'Cosmo.es', 'CrimeDistrict.fr', 'Cuatro.es', 'Cubavision.cu', 'DAZN1.es',
    'DAZN2.es', 'DKiss.es', 'DMAX.es', 'Discovery.es', 'DiscoveryChannel.fr', 'DiscoveryInvestigation.fr',
    'DiscoveryScience.fr', 'DisneyChannel.fr', 'DisneyJunior.es', 'EITBBasque.es', 'ETB1.es', 'ETB2.es',
    'ETB3.es', 'El13.ar', 'ElToroTV.es', 'ElleFictions.ca', 'Equidia.fr', 'Esport3.es',
    'Euronews.es', 'Euronews.fr', 'Eurosport1.es', 'Eurosport1.fr', 'Eurosport2.es', 'Eurosport2.fr',
    'Eurosport3601.fr', 'Explora.ca', 'France2.fr', 'France24.fr', 'France3.fr', 'France4.fr',
    'France5.fr', 'FranceInfo.fr', 'FrissonsTV.ca', 'GolfPlus.fr', 'Gulli.fr', 'Histoire.fr',
    'I24News.fr', 'ICIRadioCanadaOttawa.ca.ca', 'ICITeleMontreal.ca', 'ICITeleToronto.ca', 'IDF1.fr', 'ImagenTV.mx',
    'InfosportPlus.fr', 'Investigation.ca', 'KTO.fr', 'LA1.es', 'LA2.es', 'LAT| A&E HD',
    'LAT| AMC HD', 'LAT| AXN HD', 'LAT| BABY TV HD', 'LAT| DE PELICULA HD', 'LAT| DISCOVERY TURBO HD', 'LAT| H2 HD',
    'LAT| HISTORY 2 HD', 'LAT| LIFETIME HD', 'LAT| MULTIMEDIOS PLUS HD', 'LAT| SUNDANCE TV HD', 'LAT| UNIMAS NEW YORK HD', 'LCI.fr',
    'LEquipe.mu', 'LEquipe21.fr', 'LSV| CANAL 19', 'LSV| CANAL 6', 'LSV| MEGAVISION CANAL 21', 'LaChaineMeteo.fr',
    'LaChaineParlementaire.fr', 'LaOtra.es', 'LaSexta.es', 'LeCanalNouvelles.ca', 'M6.fr', 'M6Music.fr',
    'MAX.ca', 'MGGTV.fr', 'MPlusAccion.es', 'MPlusCineEspanol.es', 'MPlusClasicos.es', 'MPlusComedia.es',
    'MPlusDocumentales.es', 'MPlusDrama.es', 'MPlusHits.es', 'MPlusIndie.es', 'MPlusLaligaTV.es', 'MPlusLaligaTV2.es',
    'MPlusLaligaTV3.es', 'MPlusOriginales.es', 'MTV.es', 'MTV.fr', 'MTV00s.es', 'Mangas.fr',
    'MaxAvances.es', 'Mega.es', 'Mezzo.es', 'Mezzo.fr', 'MezzoLive.es', 'MezzoLive.fr',
    'Moicie.ca', 'MovistarPlus.pe', 'MovistarPlusPlus.es', 'MovistarPlusPlus2.es', 'NHKWorld.jp', 'NRJHits.fr',
    'NatGeoWild.es', 'NationalGeographic.es', 'NationalGeographic.fr', 'NavarraTV.es', 'NegociosTV.es', 'Neox.es',
    'NickJr.es', 'NickJr.fr', 'Nickelodeon.es', 'Nickelodeon.fr', 'NickelodeonJunior.fr', 'NickelodeonTeen.fr',
    'Noovo.ca', 'Nouvelles.ca', 'Nova.es', 'NovelasTV.fr', 'OCS.fr', 'OLTV.fr',
    'Odisea.es', 'OlympiaTv.fr', 'ParamountNetwork.es', 'ParisPremiere.fr', 'PeruMagico.pe', 'PiwiPlus.mu',
    'PlanetePlus.fr', 'PlanetePlusCrime.mu', 'Polar.fr', 'Prise2.ca', 'RDINews.ca', 'RDS.ca',
    'RDS2.ca', 'RDSInfo.ca', 'RFMTV.fr', 'RMCDecouverte.fr', 'RMCMystere.fr', 'RMCSport1.fr',
    'RMCSport2.fr', 'RMCTalkSport.fr', 'RMCstory.fr', 'RMCwow.fr', 'RTL9.lu', 'RTl9.mu',
    'RealMadridTV.es', 'Seasons.fr', 'Seasons.mu', 'Serieclub.fr', 'SeriesPlus.ca', 'SolMusica.es',
    'Somos.es', 'StarChannel.es', 'StarzKidsFamily.us', 'StingrayDjazz.fr', 'SuperEcran.ca', 'SuperEcran2.ca',
    'SuperEcran3.ca', 'SuperEcran4.ca', 'Syfy.fr', 'TCM.es', 'TCM.fr', 'TF1.fr',
    'TF1SeriesFilms.fr', 'TFO.ca', 'TFX.fr', 'TLC.fr', 'TMC.fr', 'TN.ar',
    'TV3.es', 'TV3Cat.es', 'TV5Monde.es', 'TV5Monde.fr', 'TVA.ca', 'TVASports.ca',
    'TVASports2.ca', 'TVCanarias.es', 'TVGEuropa.es', 'TeleQuebec.ca', 'TeleToonPlus.fr', 'Telecinco.es',
    'Teledeporte.es', 'TeletoonPlus.mu', 'Ten.es', 'Teva.fr', 'Tiji.fr', 'TouteHistoire.fr',
    'TraceAfrica.fr', 'TraceCaribbean.fr', 'TraceSportStars.fr', 'TraceUrban.fr', 'Trece.es', 'Trek.fr',
    'TvBreizh.fr', 'Ubeat.es', 'UnisTV.ca', 'UshuaiaTV.fr', 'W9.fr', 'WIPRTV.us',
    'WarnerTV.es', 'WarnerTV.fr', 'Xtrm.es', 'ZTele.ca', 'Zeste.ca', 'ca.Historia',
    'ca.ICI (CBUFT) Vancouver, BC', 'ca.RDS Info', 'ca.SRC Ottawa', 'ca.tv5-international-west', 'es.#Vamos', 'la.CGTN (CCTV4)',
    'la.Canal 2 de Panamá (TVN-2)', 'la.Canal 9 de Panamá (TVMax)', 'la.Canal A&E (Latinoamérica)', 'la.Canal AMC (México)', 'la.Canal AYM Sports', 'la.Canal America TV',
    'la.Canal Azteca Uno', 'la.Canal Baby TV', 'la.Canal CNN Internacional', 'la.Canal Capital (Colombia)', 'la.Canal De Película', 'la.Canal De Película Clásico',
    'la.Canal ESPN Deportes', 'la.Canal Fox Deportes', 'la.Canal Golden Plus', 'la.Canal Lifetime', 'la.Canal Starz Encore Español', 'la.Canal Sundance TV',
    'la.Canal TV Chile', 'la.Canal Teleamazonas', 'la.Canal Telefórmula', 'la.Canal Telemundo (México)', 'la.Canal Univision TLNovelas', 'la.Canal WAPA-TV',
    'la.Canal beIN Sport en Español', 'la.CentroAmérica TV', 'la.Discovery Turbo', 'la.TUDN', 'la.Telemundo  - Pacific Feed', 'la.Telemundo (KBLR) Las Vegas, NV',
    'la.Telemundo (KNSO) Fresno, CA', 'la.Telemundo (KTAZ) Phoenix, AZ', 'la.Telemundo (KTMD) Houston, TX', 'la.Telemundo (KVEA) Los Angeles, CA', 'la.Telemundo (KXTX) Dallas, TX', 'la.Telemundo (WKAQ) San Juan, PR',
    'la.Telemundo (WKTB-CD2) Atlanta, GA', 'la.Telemundo (WNEU) Manchester, MA HD', 'la.Telemundo (WNJU) Teterboro, NJ', 'la.Telemundo (WSCV) Fort Lauderdale, FL', 'la.Telemundo (WSNS) Chicago, IL', 'la.Telemundo (WZDC) Washington, DC',
    'la.UNI (KAKW) Austin, TX HD', 'la.UNI (KFTV) Fresno, CA', 'la.UNI (KMEX) Los Angeles, CA', 'la.UNI (KUVN) Dallas, TX', 'la.UNI (KXLN) Houston, TX', 'la.UNI (WFTY-DT2) New York, NY',
    'la.UNI (WGBO) Chicago, IL', 'la.UNI (WLTV) Miami, FL', 'la.UNI (WLTV) Miami, FL HD', 'la.UNI (WUVG) Atlanta, GA', 'la.UniMás  - Network Pacific', 'la.UniMás (KMEX-DT2) Los Angeles, CA',
    'la.UniMás (KSTR) Dallas, TX', 'la.UniMás (WFUT) New York, NY', 'la.Univision - Eastern Feed', 'la.Univision - Pacific Feed', 'mx.Canal 4 de Monterrey (XEFB-TDT)', 'mx.Canal AZ Mundo',
    'mx.Canal BitMe', 'mx.Canal Clan TVE', 'mx.Canal De Película Clásico', 'mx.Canal Golden Plus', 'mx.Canal HLN', 'mx.Canal Multimedios',
    'mx.Canal Multimedios Plus', 'mx.Canal Pasiones (Latinoamérica)', 'mx.Canal TUDN (México)', 'mx.Canal Telefórmula', 'mx.Canal Unicable (México)', 'sv.Canal 12 de El Salvador',
    'sv.Canal 2 de El Salvador', 'sv.Canal 21 de El Salvador (Megavisión)', 'sv.Canal 4 de El Salvador',
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "epg-merger"})
    data = urllib.request.urlopen(req, timeout=120).read()
    return gzip.decompress(data) if url.endswith(".gz") else data

tv = ET.Element("tv", {"generator-info-name": "epg-merger"})
seen = set(); n = 0
for url in SOURCES:
    try:
        raw = fetch(url)
    except Exception as e:
        print("WARN skip", url, e, file=sys.stderr); continue
    for _, el in ET.iterparse(io.BytesIO(raw), events=("end",)):
        if el.tag == "channel":
            cid = el.get("id", "")
            if cid in KEEP and cid not in seen:
                seen.add(cid); tv.append(el)
            else:
                el.clear()
        elif el.tag == "programme":
            if el.get("channel", "") in KEEP:
                tv.append(el); n += 1
            else:
                el.clear()

ET.ElementTree(tv).write("guide.xml", encoding="UTF-8", xml_declaration=True)
print("guide.xml:", len(seen), "channels,", n, "programmes")
if not seen:
    sys.exit("no channels matched")
