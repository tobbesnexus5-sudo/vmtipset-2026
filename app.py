import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# -- INSTÄLLNINGAR --
st.set_page_config(page_title="VM-Tipset 2026", layout="wide")
DEADLINE = datetime(2026, 6, 11, 0, 0)
DATA_FILE = "tips_data.json"

# -- ALLA 72 MATCHER --
INITIAL_MATCHES = [
  { "id": 1, "datum": "11/6", "grp": "A", "tid": "21:00", "match": "Mexiko – Sydafrika", "kanal": "TV4" },
  { "id": 2, "datum": "12/6", "grp": "A", "tid": "04:00", "match": "Sydkorea – Tjeckien", "kanal": "TV4" },
  { "id": 3, "datum": "12/6", "grp": "B", "tid": "21:00", "match": "Kanada – Bosnien och Hercegovina", "kanal": "SVT" },
  { "id": 4, "datum": "13/6", "grp": "D", "tid": "03:00", "match": "USA – Paraguay", "kanal": "TV4" },
  { "id": 5, "datum": "13/6", "grp": "B", "tid": "21:00", "match": "Qatar – Schweiz", "kanal": "TV4" },
  { "id": 6, "datum": "14/6", "grp": "C", "tid": "00:00", "match": "Brasilien – Marocko", "kanal": "SVT" },
  { "id": 7, "datum": "14/6", "grp": "C", "tid": "03:00", "match": "Haiti – Skottland", "kanal": "SVT" },
  { "id": 8, "datum": "14/6", "grp": "D", "tid": "06:00", "match": "Australien – Turkiet", "kanal": "TV4" },
  { "id": 9, "datum": "14/6", "grp": "E", "tid": "19:00", "match": "Tyskland – Curacao", "kanal": "TV4" },
  { "id": 10, "datum": "14/6", "grp": "F", "tid": "22:00", "match": "Nederländerna – Japan", "kanal": "TV4" },
  { "id": 11, "datum": "15/6", "grp": "E", "tid": "01:00", "match": "Elfenbenskusten – Ecuador", "kanal": "TV4" },
  { "id": 12, "datum": "15/6", "grp": "F", "tid": "04:00", "match": "Sverige – Tunisien", "kanal": "SVT" },
  { "id": 13, "datum": "15/6", "grp": "H", "tid": "18:00", "match": "Spanien – Kap Verde", "kanal": "SVT" },
  { "id": 14, "datum": "15/6", "grp": "G", "tid": "21:00", "match": "Belgien – Egypten", "kanal": "SVT" },
  { "id": 15, "datum": "16/6", "grp": "H", "tid": "00:00", "match": "Saudiarabien – Uruguay", "kanal": "TV4" },
  { "id": 16, "datum": "16/6", "grp": "G", "tid": "03:00", "match": "Iran – Nya Zeeland", "kanal": "TV4" },
  { "id": 17, "datum": "16/6", "grp": "I", "tid": "21:00", "match": "Frankrike – Senegal", "kanal": "SVT" },
  { "id": 18, "datum": "17/6", "grp": "I", "tid": "00:00", "match": "Irak – Norge", "kanal": "TV4" },
  { "id": 19, "datum": "17/6", "grp": "J", "tid": "03:00", "match": "Argentina – Algeriet", "kanal": "TV4" },
  { "id": 20, "datum": "17/6", "grp": "J", "tid": "06:00", "match": "Österrike – Jordanien", "kanal": "TV4" },
  { "id": 21, "datum": "17/6", "grp": "K", "tid": "19:00", "match": "Portugal – DR Kongo", "kanal": "TV4" },
  { "id": 22, "datum": "17/6", "grp": "L", "tid": "22:00", "match": "England – Kroatien", "kanal": "TV4" },
  { "id": 23, "datum": "18/6", "grp": "L", "tid": "01:00", "match": "Ghana – Panama", "kanal": "TV4" },
  { "id": 24, "datum": "18/6", "grp": "K", "tid": "04:00", "match": "Uzbekistan – Colombia", "kanal": "TV4" },
  { "id": 25, "datum": "18/6", "grp": "A", "tid": "18:00", "match": "Tjeckien – Sydafrika", "kanal": "TV4" },
  { "id": 26, "datum": "18/6", "grp": "B", "tid": "21:00", "match": "Schweiz – Bosnien och Hercegovina", "kanal": "TV4" },
  { "id": 27, "datum": "19/6", "grp": "B", "tid": "00:00", "match": "Kanada – Qatar", "kanal": "TV4" },
  { "id": 28, "datum": "19/6", "grp": "A", "tid": "03:00", "match": "Mexiko – Sydkorea", "kanal": "TV4" },
  { "id": 29, "datum": "19/6", "grp": "D", "tid": "21:00", "match": "USA – Australien", "kanal": "SVT" },
  { "id": 30, "datum": "20/6", "grp": "C", "tid": "00:00", "match": "Skottland – Marocko", "kanal": "SVT" },
  { "id": 31, "datum": "20/6", "grp": "C", "tid": "02:30", "match": "Brasilien – Haiti", "kanal": "TV4" },
  { "id": 32, "datum": "20/6", "grp": "D", "tid": "05:00", "match": "Turkiet – Paraguay", "kanal": "TV4" },
  { "id": 33, "datum": "20/6", "grp": "F", "tid": "19:00", "match": "Nederländerna – Sverige", "kanal": "TV4" },
  { "id": 34, "datum": "20/6", "grp": "E", "tid": "22:00", "match": "Tyskland – Elfenbenskusten", "kanal": "TV4" },
  { "id": 35, "datum": "21/6", "grp": "E", "tid": "02:00", "match": "Ecuador – Curaçao", "kanal": "TV4" },
  { "id": 36, "datum": "21/6", "grp": "F", "tid": "06:00", "match": "Tunisien – Japan", "kanal": "SVT" },
  { "id": 37, "datum": "21/6", "grp": "H", "tid": "18:00", "match": "Spanien – Saudiarabien", "kanal": "TV4" },
  { "id": 38, "datum": "21/6", "grp": "G", "tid": "21:00", "match": "Belgien – Iran", "kanal": "TV4" },
  { "id": 39, "datum": "22/6", "grp": "H", "tid": "00:00", "match": "Uruguay – Kap Verde", "kanal": "TV4" },
  { "id": 40, "datum": "22/6", "grp": "G", "tid": "03:00", "match": "Nya Zeeland – Egypten", "kanal": "TV4" },
  { "id": 41, "datum": "22/6", "grp": "J", "tid": "19:00", "match": "Argentina – Österrike", "kanal": "SVT" },
  { "id": 42, "datum": "22/6", "grp": "I", "tid": "23:00", "match": "Frankrike – Irak", "kanal": "SVT" },
  { "id": 43, "datum": "23/6", "grp": "I", "tid": "02:00", "match": "Norge – Senegal", "kanal": "SVT" },
  { "id": 44, "datum": "23/6", "grp": "J", "tid": "05:00", "match": "Jordanien – Algeriet", "kanal": "TV4" },
  { "id": 45, "datum": "23/6", "grp": "K", "tid": "19:00", "match": "Portugal – Uzbekistan", "kanal": "SVT" },
  { "id": 46, "datum": "23/6", "grp": "L", "tid": "22:00", "match": "England – Ghana", "kanal": "SVT" },
  { "id": 47, "datum": "24/6", "grp": "L", "tid": "01:00", "match": "Panama – Kroatien", "kanal": "TV4" },
  { "id": 48, "datum": "24/6", "grp": "K", "tid": "04:00", "match": "Colombia – DR Kongo", "kanal": "TV4" },
  { "id": 49, "datum": "24/6", "grp": "B", "tid": "21:00", "match": "Schweiz – Kanada", "kanal": "TV4" },
  { "id": 50, "datum": "24/6", "grp": "B", "tid": "21:00", "match": "Bosnien och Hercegovina – Qatar", "kanal": "TV4" },
  { "id": 51, "datum": "25/6", "grp": "C", "tid": "00:00", "match": "Marocko – Haiti", "kanal": "TV4" },
  { "id": 52, "datum": "25/6", "grp": "C", "tid": "00:00", "match": "Skottland – Brasilien", "kanal": "TV4" },
  { "id": 53, "datum": "25/6", "grp": "A", "tid": "03:00", "match": "Sydafrika – Sydkorea", "kanal": "SVT" },
  { "id": 54, "datum": "25/6", "grp": "A", "tid": "03:00", "match": "Tjeckien – Mexiko", "kanal": "SVT" },
  { "id": 55, "datum": "25/6", "grp": "E", "tid": "22:00", "match": "Curacao – Elfenbenskusten", "kanal": "SVT" },
  { "id": 56, "datum": "25/6", "grp": "E", "tid": "22:00", "match": "Ecuador – Tyskland", "kanal": "SVT" },
  { "id": 57, "datum": "26/6", "grp": "F", "tid": "01:00", "match": "Tunisien – Nederländerna", "kanal": "SVT" },
  { "id": 58, "datum": "26/6", "grp": "F", "tid": "01:00", "match": "Japan – Sverige", "kanal": "SVT" },
  { "id": 59, "datum": "26/6", "grp": "D", "tid": "04:00", "match": "Turkiet – USA", "kanal": "TV4" },
  { "id": 60, "datum": "26/6", "grp": "D", "tid": "04:00", "match": "Paraguay – Australien", "kanal": "TV4" },
  { "id": 61, "datum": "26/6", "grp": "I", "tid": "21:00", "match": "Norge – Frankrike", "kanal": "TV4" },
  { "id": 62, "datum": "26/6", "grp": "I", "tid": "21:00", "match": "Senegal – Irak", "kanal": "TV4" },
  { "id": 63, "datum": "27/6", "grp": "H", "tid": "02:00", "match": "Kap Verde – Saudiarabien", "kanal": "TV4" },
  { "id": 64, "datum": "27/6", "grp": "H", "tid": "02:00", "match": "Uruguay – Spanien", "kanal": "TV4" },
  { "id": 65, "datum": "27/6", "grp": "G", "tid": "05:00", "match": "Nya Zeeland – Belgien", "kanal": "TV4" },
  { "id": 66, "datum": "27/6", "grp": "G", "tid": "05:00", "match": "Egypten – Iran", "kanal": "TV4" },
  { "id": 67, "datum": "27/6", "grp": "L", "tid": "23:00", "match": "Panama – England", "kanal": "SVT" },
  { "id": 68, "datum": "27/6", "grp": "L", "tid": "23:00", "match": "Kroatien – Ghana", "kanal": "SVT" },
  { "id": 69, "datum": "28/6", "grp": "K", "tid": "01:30", "match": "Demokratiska republiken Kongo – Uzbekistan", "kanal": "TV4" },
  { "id": 70, "datum": "28/6", "grp": "K", "tid": "01:30", "match": "Colombia – Portugal", "kanal": "TV4" },
  { "id": 71, "datum": "28/6", "grp": "J", "tid": "04:00", "match": "Algeriet – Österrike", "kanal": "TV4" },
  { "id": 72, "datum": "28/6", "grp": "J", "tid": "04:00", "match": "Jordanien – Argentina", "kanal": "TV4" }
]

# -- DATABASHANTERING (JSON) --
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"profiles": {}, "facit": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# -- NAVIGERING --
menu = st.sidebar.radio("Meny", ["🏆 Startsida (Topplista)", "📝 Skapa ditt tips", "⚙️ Hantera profil", "🔒 Admin: Fyll i Facit"])

# -- 1. STARTSIDA --
if menu == "🏆 Startsida (Topplista)":
    st.title("🏆 VM-Tipset 2026 - Leaderboard")
    
    # Regelruta
    st.info("""
    **VM-tipset går ut på att:**
    Tippa rätt resultat (1, X, 2) i samtliga 72 gruppspelsmatcher. Vinner gör den som har flest antal rätt. 
    Om flera hamnar på samma antal rätt avgör utslagsfrågan.
    
    **Utslagsfråga:**
    Hur många mål görs det totalt under hela fotbolls-VM, totalt 104 matcher?
    *(gäller mål under ordinarie tid, ej under förlängning och straffsparkar)*
    
    **Vinstpotten:** Delas på nr 1 (70 %) och nr 2 (30 %).
    **Insats:** 200 kr.
    """)

    if not data["profiles"]:
        st.write("Inga profiler skapade ännu. Bli först!")
    else:
        scores = []
        for name, profile_data in data["profiles"].items():
            score = 0
            tips = profile_data.get("tips", {})
            tiebreaker = profile_data.get("tiebreaker", "-")
            
            for match in INITIAL_MATCHES:
                match_id = str(match["id"])
                if match_id in data["facit"] and data["facit"][match_id] == tips.get(match_id):
                    score += 1
            scores.append({"Namn": name, "Utslagsfråga (Mål)": tiebreaker, "Poäng": score})
        
        df = pd.DataFrame(scores).sort_values(by="Poäng", ascending=False).reset_index(drop=True)
        df.index += 1
        st.dataframe(df, use_container_width=True)

# -- 2. SKAPA PROFIL --
elif menu == "📝 Skapa ditt tips":
    st.title("Skapa ditt tips")
    
    if datetime.now() > DEADLINE:
        st.error("Tiden har gått ut! VM har startat.")
    else:
        st.warning("⚠️ **Glöm inte insatsen!** 200 kr betalas till Christer.K när du lagt ditt tips.")
        with st.form("create_form"):
            namn = st.text_input("Ditt Namn *")
            
            st.write("---")
            st.write("**Utslagsfråga ***")
            st.write("Hur många mål görs det totalt under hela fotbolls-VM, totalt 104 matcher? (gäller mål under ordinarie tid, ej under förlängning och straffsparkar)")
            tiebreaker_input = st.number_input("Antal mål:", min_value=0, step=1, value=0)
            
            st.write("---")
            st.write("Fyll i 1, X eller 2 för varje match nedan:")
            
            # Skapa tabell för input
            df_matches = pd.DataFrame(INITIAL_MATCHES)
            df_matches["Ditt Tips (1, X, 2)"] = ""
            df_display = df_matches[["datum", "tid", "match", "kanal", "Ditt Tips (1, X, 2)"]]
            
            redigerad_df = st.data_editor(df_display, use_container_width=True, hide_index=True)
            
            submitted = st.form_submit_button("Spara Tips")
            
            if submitted:
                if not namn.strip():
                    st.error("Du måste fylla i ett namn.")
                elif namn.strip() in data["profiles"]:
                    st.error("Namnet finns redan.")
                elif tiebreaker_input <= 0:
                     st.error("Du måste fylla i ett giltigt antal mål på utslagsfrågan (mer än 0).")
                else:
                    alla_fyllda = True
                    tips_dict = {}
                    for i, row in redigerad_df.iterrows():
                        tips = str(row["Ditt Tips (1, X, 2)"]).strip().upper()
                        if tips not in ["1", "X", "2"]:
                            alla_fyllda = False
                        tips_dict[str(INITIAL_MATCHES[i]["id"])] = tips
                        
                    if not alla_fyllda:
                        st.error("Du måste fylla i 1, X eller 2 på ALLA 72 matcher!")
                    else:
                        data["profiles"][namn.strip()] = {
                            "tips": tips_dict,
                            "tiebreaker": int(tiebreaker_input)
                        }
                        save_data(data)
                        st.success(f"Tack för ditt tips, {namn.strip()}! Glöm inte att swisha 200 kr till Christer.K.")
                        st.balloons()

# -- 3. HANTERA PROFIL --
elif menu == "⚙️ Hantera profil":
    st.title("Hantera profil")
    if not data["profiles"]:
        st.warning("Inga profiler finns.")
    else:
        vald_profil = st.selectbox("Välj profil:", list(data["profiles"].keys()))
        
        if vald_profil:
            profile_data = data["profiles"][vald_profil]
            tips = profile_data.get("tips", {})
            current_tiebreaker = profile_data.get("tiebreaker", "-")
            
            if datetime.now() > DEADLINE:
                st.info("🔒 Redigering är nu stängd. VM har startat!")
                st.write(f"**Utslagsfråga:** {current_tiebreaker} mål")
                
                # Visa nuvarande tips och jämför med facit
                visnings_lista = []
                for m in INITIAL_MATCHES:
                    match_id = str(m["id"])
                    visnings_lista.append({
                        "Match": m["match"],
                        "Tippat": tips.get(match_id, ""),
                        "Facit": data["facit"].get(match_id, "")
                    })
                st.dataframe(pd.DataFrame(visnings_lista), use_container_width=True, hide_index=True)
            else:
                st.write("Här kan du granska och redigera dina lagda tips fram tills att VM startar.")
                
                # ---- NY KOD FÖR ATT VISA TIPS VS FACIT INNAN REDIGERING LÅSES ----
                # Lägg in visningsläget här också, innan man klickar på att redigera.
                st.write(f"**Utslagsfråga:** {current_tiebreaker} mål")
                visnings_lista = []
                for m in INITIAL_MATCHES:
                    match_id = str(m["id"])
                    visnings_lista.append({
                        "Match": m["match"],
                        "Tippat": tips.get(match_id, ""),
                        "Facit": data["facit"].get(match_id, "")
                    })
                
                # Vi visar en skrivskyddad tabell först, sedan har vi redigeringsformuläret i en expander
                st.dataframe(pd.DataFrame(visnings_lista), use_container_width=True, hide_index=True)
                
                with st.expander("Redigera dina tips"):
                    with st.form("edit_form"):
                        st.write(f"**Redigerar tips för:** {vald_profil}")
                        
                        edit_tiebreaker = st.number_input(
                            "Utslagsfråga (Totalt antal mål i VM):", 
                            min_value=0, 
                            step=1, 
                            value=int(current_tiebreaker) if str(current_tiebreaker).isdigit() else 0
                        )
                        
                        st.write("Fyll i 1, X eller 2 nedan:")
                        
                        # Förbered redigeringslistan
                        edit_list = []
                        for m in INITIAL_MATCHES:
                            match_id = str(m["id"])
                            edit_list.append({
                                "datum": m["datum"],
                                "tid": m["tid"],
                                "match": m["match"],
                                "kanal": m["kanal"],
                                "Ditt Tips (1, X, 2)": tips.get(match_id, "")
                            })
                            
                        df_edit = pd.DataFrame(edit_list)
                        redigerad_df = st.data_editor(df_edit, use_container_width=True, hide_index=True)
                        
                        submitted_edit = st.form_submit_button("Spara Ändringar")
                        
                        if submitted_edit:
                            if edit_tiebreaker <= 0:
                                st.error("Du måste fylla i ett giltigt antal mål på utslagsfrågan (mer än 0).")
                            else:
                                alla_fyllda = True
                                new_tips_dict = {}
                                for i, row in redigerad_df.iterrows():
                                    t = str(row["Ditt Tips (1, X, 2)"]).strip().upper()
                                    if t not in ["1", "X", "2"]:
                                        alla_fyllda = False
                                    new_tips_dict[str(INITIAL_MATCHES[i]["id"])] = t
                                    
                                if not alla_fyllda:
                                    st.error("Alla 72 matcher måste vara ifyllda med 1, X eller 2!")
                                else:
                                    data["profiles"][vald_profil] = {
                                        "tips": new_tips_dict,
                                        "tiebreaker": int(edit_tiebreaker)
                                    }
                                    save_data(data)
                                    st.success("Ändringarna har sparats!")
                                    st.rerun()
                # -------------------------------------------------------------------

            st.divider()
            
            # Ta bort
            if st.checkbox("Jag vill ta bort profilen permanent"):
                if st.button("🚨 Radera nu"):
                    del data["profiles"][vald_profil]
                    save_data(data)
                    st.success("Profil raderad.")
                    st.rerun()

# -- 4. ADMIN: FACIT --
elif menu == "🔒 Admin: Fyll i Facit":
    st.title("Fyll i Matchresultat")
    st.write("Resultaten du fyller i här uppdaterar topplistan.")
    
    df_matches = pd.DataFrame(INITIAL_MATCHES)
    df_matches["Resultat"] = [data["facit"].get(str(m["id"]), "") for m in INITIAL_MATCHES]
    df_display = df_matches[["datum", "match", "Resultat"]]
    
    redigerad_df = st.data_editor(df_display, use_container_width=True, hide_index=True)
    
    if st.button("Spara Facit"):
        for i, row in redigerad_df.iterrows():
            res = str(row["Resultat"]).strip().upper()
            if res in ["1", "X", "2", ""]:
                 data["facit"][str(INITIAL_MATCHES[i]["id"])] = res
        save_data(data)
        st.success("Facit uppdaterat!")
