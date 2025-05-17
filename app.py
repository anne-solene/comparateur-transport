### Created by Anne-Solene Bornens on May 16th 2025

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_extras.let_it_rain import rain 
#from textblob import TextBlob

st.markdown("## Jacques a dit : « Il n'y a d'acte que signifiant. »")

ballons = st.text_input("Aimez-vous les ballons de baudruche ?", None)
if ballons in ['oui', 'OUI', 'Oui']:
	#rain(
        #emoji="🎈",
        #font_size=54,
        #falling_speed=5,
        #animation_length="infinite",
    )
	st.ballons()
	st.markdown("🎈🎈🎈 Oh super, plein de ballons ! 🎈🎈🎈")
elif ballons is not None:
	st.markdown("Ok, je peux comprendre. Allez on passe aux choses sérieuses.")
	
# Interface utilisateur (sliders)
st.sidebar.header("Paramètres")

st.sidebar.subheader("Pass Navigo")
navigo_tarif_mensuel = st.sidebar.slider("Tarif mensuel (€)", 0.0, 100.0, 88.8, step=0.1)
navigo_taux_remboursement_CRR = st.sidebar.slider("Taux de remboursement par le CRR (%)", 0, 100, 50, step=1)

st.sidebar.subheader("Parking Hôtel de Ville (Q-Park)")
hv_nb_jours = st.sidebar.slider("Nombre de jours par semaine", 0, 5, 1, step=1, key="jours_hv")
hv_tarif_jour = st.sidebar.slider("Tarif journée (€)", 0.0, 50.0, 39.8, step=0.1, key="prix1J_hv")
hv_abonnement_5 = st.sidebar.slider("Tarif abonnement 5 jours (€)", 0, 200, 145, step=1)
hv_abonnement_7 = st.sidebar.slider("Tarif abonnement 7 jours (€)", 0, 200, 179, step=1)

st.sidebar.subheader("Parking Belle-Feuille (Indigo)")
bf_nb_jours = st.sidebar.slider("Nombre de jours par semaine", 0, 5, 1, step=1, key="jours_bf")
bf_tarif_jour = st.sidebar.slider("Tarif journée (€)", 0.0, 50.0, 18.4, step=0.1, key="prix1J_bf")

mois = 12
semaines_par_mois = 4.33
semaines_travaillees = 36

# Calcul du coût selon la situation de remboursement

resultats = {}
navigo_total = navigo_tarif_mensuel * mois
navigo_total_rembourse = navigo_total * (1 - navigo_taux_remboursement_CRR*0.01)

resultats['Avec remboursement Hôtel de Ville'] = (navigo_total + 
					bf_nb_jours * semaines_travaillees * bf_tarif_jour)

resultats['Avec remboursement Belle-Feuille'] = (navigo_total +
                    hv_nb_jours * semaines_travaillees * hv_tarif_jour)

resultats['Avec remboursement du Pass Navigo, abonnement 7/24 Hôtel de Ville'] = (navigo_total_rembourse +
                    hv_abonnement_7 * 10 +
                    bf_nb_jours * semaines_travaillees * bf_tarif_jour)

resultats["Avec remboursement du Pass Navigo, abonnement 'Bureau' Hôtel de Ville"] = (navigo_total_rembourse +
                    hv_abonnement_5 * 10 +
                    bf_nb_jours * semaines_travaillees * bf_tarif_jour)

resultats['Avec remboursement du Pass Navigo, sans abonnement au parking'] = (navigo_total_rembourse +
                    hv_nb_jours * semaines_travaillees * hv_tarif_jour +
                    bf_nb_jours * semaines_travaillees * bf_tarif_jour)

resultats['Sans aucun remboursement'] = (navigo_total +
                    hv_nb_jours * semaines_travaillees * hv_tarif_jour +
                    bf_nb_jours * semaines_travaillees * bf_tarif_jour)

# Affichage des résultats sous forme de diagramme en barres
st.markdown("### 🔎 Comparaison des scénarios de coût Navigo/Parking")

categories = list(resultats.keys())
valeurs = list(resultats.values())

#fig, ax = plt.subplots()
#ax.barh(categories, valeurs, color='skyblue')
#ax.set_xlabel("Coût total annuel (€)")
#ax.set_title("Comparaison des coûts selon les scénarios")
#st.pyplot(fig)

def wrap_label(label, max_words=5):
    words = label.split()
    lines = []
    for i in range(0, len(words), max_words):
        lines.append(" ".join(words[i:i+max_words]))
    return "<br>".join(lines)

# Appliquer le wrapping à chaque légende
categorie_min = min(resultats, key=resultats.get)
categorie_max = max(resultats, key=resultats.get)
categories_wrapped = [wrap_label(cat, max_words=5) for cat in categories]
couleur_standard = 'rgba(10, 50, 100, 0.85)'  # bleu marine
couleur_actuel = 'rgba(80, 150, 255, 0.85)'  # bleu autre 
couleur_pas_cher = 'rgba(46, 204, 113, 0.85)'  # vert foncé
couleur_cher = 'rgba(255, 75, 75, 0.85)'  # rouge foncé
colors = [
    couleur_actuel if cat == 'Avec remboursement du Pass Navigo, sans abonnement au parking' else couleur_cher if cat == categorie_max else
    couleur_pas_cher if cat == categorie_min else couleur_standard
    for cat in categories
]

fig = go.Figure(go.Bar(
    x=valeurs,
    y=categories_wrapped,
    orientation='h',
    marker=dict(color=colors),
    hovertemplate='%{y} : %{x:.2f} €<extra></extra>'
))

fig.update_layout(
    xaxis_title="Coût total annuel (€)",
    yaxis_title="",
    #title="Comparaison des coûts selon les scénarios",
    template="simple_white",
    height=400,
    margin=dict(l=120, r=20, t=50, b=40),
	font=dict(
        size=16,              # Taille globale du texte (plus grande)
        color="rgb(60, 60, 60)"  # Gris foncé
    ),
    xaxis=dict(
        title_font=dict(size=16, color='rgb(60, 60, 60)'),
        tickfont=dict(size=14, color='rgb(50, 50, 50)')
    ),
    yaxis=dict(
        tickfont=dict(size=14, color='rgb(50, 50, 50)')
    )
)

st.plotly_chart(fig, use_container_width=True)
# Affichage de la situation la plus économique
cout_min = resultats[categorie_min]
cout_max = resultats[categorie_max]
gain = resultats['Avec remboursement du Pass Navigo, sans abonnement au parking'] - cout_min

st.markdown("### 💡 Conclusions du conseiller financier :")
st.success(f"La situation la plus économique à l'année est **{categorie_min}** : coût annuel de **{cout_min:.2f} €**. Par rapport à la situation actuelle, vous gagneriez environ {gain:.2f}€ par an. C'est tout de même l'équivalent d'environ {gain/11:.0f} salades...! ")
st.error(f"La situation la moins stratégique économiquement à l'année est **{categorie_max}** : coût annuel de **{cout_max:.2f} €**. Dans la situation actuelle, vous évitez donc déjà {cout_max - resultats['Avec remboursement du Pass Navigo, sans abonnement au parking']:.2f}€ de pertes supplémentaires possibles. C'est un bon début, j'imagine.")
st.info("Probablement s'imagine-t-on qu'il vaut mieux suivre les recommandations sous-entendues par l'encadré vert. Mais faut-il toujours suivre le bon sens ? Plus encore, faire le choix de la raison, n'est-ce pas déjà se soumettre au regard moral des hommes ? Dès lors, l'éthique doit-elle être invoquée dans les actions pratiques du quotidien ? Et puisque Wittgenstein a pu dire qu'« éthique et esthétique sont une seule et même chose », faut-il encore conclure que préférer l'Op.109 à l'Op.110 peut relever d'une même démarche que demander le remboursement d'un parking plutôt que d'un Pass Navigo ? Le choix, tout comme le non-choix, vous revient seul. Souvenons-nous à cette occasion que non seulement tout acte est signifiant, mais que dans l'acte, le signifiant est le sujet lui-même... sacré Jacques... Allez hop, au dodo.")
