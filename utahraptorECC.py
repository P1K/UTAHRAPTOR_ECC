#! /usr/local/bin/python3

import tweepy
import os
import random
import time
import datetime
import base64

# static data for small cadavre exquis
subList = ["Le chat", "Le hamster", "Le furet", "Le canard", "Le régicide", "Le matelas", "Le tricot", "Le tatou", "Le téléphérique", "Le tyran", "Le cosmos", "Le caribou", "Le débat", "Le cabri", "Le géant", "Le hussard", "Le cavalier", "Le zénith"]
subList += ["Le conspirateur", "Le palefroi", "Le soleil", "Le glaive", "Le tapioca", "Le capitaine de frégate", "Le totem", "Le nénuphar", "Le vizir", "Le lynx", "Le tribunal", "Le mythe", "Le chocolat", "Le tutoiement", "Le vin", "Le craquement"]
subList += ["Le clair de lune", "L'orfraie", "Le hibou", "L'autour", "Le funambule", "Le dompteur", "Le vent", "Le produit scalaire", "Le sophiste", "Le bulldozer", "Le bon usage", "Le maître d'hôtel", "Le ouahouah", "L'anneau unique"]
subList += ["Le menuet", "Le sténographe", "Le support", "Le domaine", "Le traversin", "L'ingénieur de l'armement", "Le turban", "L'héliport", "Le cacatois", "Le crible à corps de nombre", "Le kiwi"]
adjList = ["bleu", "blanc", "brun", "content", "mécontent", "heureux", "joli", "curieux", "trépassé", "chatoyant", "paresseux", "malin", "vertical", "absent", "sublunaire", "grotesque", "suranné", "sceptique", "original", "secret", "vivant", "gourmand"]
adjList += ["discret", "agile", "rapide", "sophistiqué", "masqué", "encapuchonné", "petit", "réduit", "malade", "vert", "mielleux", "sournois", "chafouin", "loquace", "rétif", "ténébreux"]
adjList += ["fuchsia", "pédant", "verbeux", "courroucé", "astral", "implémentable", "en temps constant", "déterministe", "arboricole", "niais", "socratique", "nacré", "bien élevé", "en temps polynomial", "armoricain", "à coulisse"]
adjList += ["fleuri", "surexponentiel", "infâme", "biadmissible", "interzone", "gazéifié au gaz de la source", "rigide", "de caractéristique deux", "menu", "stupéfait", "concupiscent", "grivois", "stoïque"]
adjList += ["capharnaümique", "hétéroclite", "flexible", "factice", "parfait", "rebelle", "spontané", "apocryphe", "in-folio", "primitif", "à l'odeur d'amande", "azoté", "voyageant à Mach 2,7", "imperméable", "trop académique pour EUROCRYPT"]
adjList += ["en grand uniforme", "façon grand veneur", "à la confiture d'airelles", "géométrique", "farceur"]
verbList = ["mange", "oriente", "chante", "libère", "invente", "gesticule", "louvoie", "raconte", "serpente", "évite", "risque", "falsifie", "conduit", "pilote", "moque", "distribue", "conseille", "dissoud", "organise", "trace", "fusionne"]
verbList += ["a", "court vers", "multiplie", "observe", "milite pour", "désire", "abandonne", "espère", "combat", "repose", "arrache", "suit", "admire", "convoite", "questionne", "vérifie", "écrit", "compose", "ourdit", "chuchote"]
verbList += ["godille", "tricote", "déracine", "crépite", "bémolise", "pourchasse", "néglige", "rapetasse", "négocie", "fustige", "escroque", "nourrit", "créance", "courtise", "provoque en duel", "remet en question", "dépêche"]
verbList += ["décorrèle", "modère", "agresse", "frustre", "démène", "exécute"]
objList = ["un lapin", "un immeuble", "un arbre", "un téléscope", "un artichaut", "un videpoche", "un cheval", "un toboggan", "un scoubidou", "un tricératops", "un koala", "un tapis", "un adversaire", "un ruban", "un fil", "un arbitre", "un fabliaux"]
objList += ["un réseau", "un chiffre", "un ordinateur", "un glacier", "un vélo", "un saladier", "un noyau", "un fantôme", "un luth", "un renard fou", "un voilier", "un sousmarin", "un mouton", "un coquelicot", "un support", "un rapide", "un artefact"]
objList += ["un ours", "un rhododendron", "un appareil", "un cirrus", "un bouchon", "un centaure", "un être émotif", "un engin lunaire", "un MAC", "un ecureuil", "un lbw", "un pantalon", "un tractopelle", "un coupon", "un bonbon", "du cobalt"]
objList += ["un corps premier", "un strapontin", "un rocher", "un lycanthrope", "un oreiller", "un exégète", "un chausson", "un nœud-papillon", "un hortensia", "un aphorisme", "un in-quarto", "un incunable"]
objList += ["un film d'espionnage", "un origami", "un sabre lumineux", "un logarithme discret", "un test match", "un ultra marathon", "un wombat", "un farfadet"]

# Cadavre exquis part, for more beautiful (very limited) randomness
# currently with fixed grammar
def createCE():
	subject = subList[random.randint(0,len(subList) - 1)]
	adjective1 = adjList[random.randint(0,len(adjList) -1 )]
	verb = verbList[random.randint(0,len(verbList) - 1)]
	obj = objList[random.randint(0,len(objList) - 1)]
	adjective2 = adjList[random.randint(0,len(adjList) - 1)]
	return subject+" "+adjective1+" "+verb+" "+obj+" "+adjective2+"."


# twitter API setup
# mersenne twister setup
# tokens are SECRET!!
def setup():
	random.seed(os.urandom(8))
	auth = tweepy.OAuthHandler("fill-me", "fill-me-too")
	auth.set_access_token("fill-me-too-too", "fill-me-too-too-too")
	api = tweepy.API(auth)
	return api

def getTokens(msg):
	toks = []
	tok = ""
	for i in range(len(msg)):
		if msg[i] == " ":
			if tok != "":
				toks.append(tok)
				tok = ""
		else:
			tok += msg[i]
	if tok != "":
		toks.append(tok)
		tok = ""
	return toks

# only returns the FIRST hashTag
def getHashTag(msg):
	words = getTokens(msg)
	for i in range(len(words)):
		if words[i][0] == "#":
			return words[i]
	return "#empty"

def isStartAnnounce(msg):
	words = getTokens(msg)
	for i in range(len(words)):
		if words[i] == "tweeting":
			return True
	return False

def isEndAnnounce(msg):
	words = getTokens(msg)
	for i in range(len(words)):
		if words[i] == "over.":
			return True
	return False

def getCurveHash(api,dateS):
	trx_tweets = api.search("from:random_zoo since:"+dateS)
	hashTag = "#empty"
	for i in range(len(trx_tweets)):
		tw = trx_tweets[i].text
		if isStartAnnounce(tw):
			hashTag = getHashTag(tw)
		if isEndAnnounce(tw):
			return "#nomore"
	return hashTag

def genCurveTweet(curveHash):
	tw = "Entropy for curve "+curveHash+" : "
	tw += createCE() + " "
	tw = tw[0:140]
	randlen = 140 - len(tw)
	randomS = str(base64.b85encode(os.urandom(randlen)))
	randomS = randomS[2:len(randomS) - 1]
	randomS = randomS[0:randlen]
	tw += randomS
	return tw


def main():
	api = setup()
	date  = datetime.date.today()
	dateS = str(date.year)+"-"+str(date.month)+"-"+str(date.day)

	# Well, of course you can improve this
	while True:
		curveHash = getCurveHash(api, dateS)
		if curveHash == "#nomore":
			print("My job is done for today. "+createCE())
			return
		elif curveHash == "#empty":
			print("Nothing for now ("+time.ctime()+"). "+createCE())
			time.sleep(100)
		else:
			tw = genCurveTweet(curveHash)
			randLat = random.uniform(-90,90)
			randLong = random.uniform(-180,180)
			api.update_status(tw,lat=randLat,long=randLong)
			time.sleep(60)
	return

main()
