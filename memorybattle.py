# MEMORY BATTLE – pit your best memories against each other
import streamlit as st, pandas as pd, random, os
from datetime import datetime
st.set_page_config(page_title="Memory Battle", layout="centered")

DATA="mb_leaderboard.csv"; PASSWORD="vortexmaster2025"
rating=["Joy","Nostalgia","Excitement","Lesson","Clarity"]

memories=[{"title":"First bike ride"},{"title":"Beach sunset 2023"},
          {"title":"Winning the school cup"},{"title":"Road-trip 2022"}]

ss=st.session_state
if "mem" not in ss: ss.mem=memories.copy()
if "duel" not in ss: ss.duel=random.sample(ss.mem,2)
if "hist" not in ss: ss.hist=[]

def pick(): ss.duel=random.sample(ss.mem,2)
def load(): return pd.read_csv(DATA) if os.path.exists(DATA) else \
    pd.DataFrame(columns=["Memory A","Memory B","Winner","Score A","Score B","Time",*rating])
def save(d): d.to_csv(DATA,index=False)

st.title("🧠 Memory Battle")

with st.sidebar.expander("➕ Add Memory"):
    t=st.text_input("Memory Title")
    if st.button("Add") and t: ss.mem.append({"title":t}); st.success(f"'{t}' added!")

mA,mB=ss.duel
st.subheader(f"🔵 {mA['title']}  vs  🟣 {mB['title']}")

rA,rB={},{}
for f in rating:
    l,r=st.columns(2)
    rA[f]=l.slider(f"{f} – A",1,10,5)
    rB[f]=r.slider(f"{f} – B",1,10,5)

if st.button("Submit"):
    sA,sB=sum(rA.values()),sum(rB.values())
    win=mA['title'] if sA>sB else mB['title'] if sB>sA else "Tie"
    row={"Memory A":mA['title'],"Memory B":mB['title'],"Winner":win,
         "Score A":sA,"Score B":sB,"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),
         **({f:rA[f] if sA>=sB else rB[f] for f in rating})}
    save(pd.concat([load(),pd.DataFrame([row])],ignore_index=True))
    ss.hist.append(f"{mA['title']} vs {mB['title']} – Winner {win} ({sA}-{sB})")
    st.success(f"Winner: {win}"); pick(); st.experimental_rerun()

st.markdown("---"); st.subheader("🏆 Recent Battles")
st.dataframe(load().tail(20).iloc[::-1], use_container_width=True)
with st.expander("📜 History"): [st.write(x) for x in ss.hist[::-1]]

with st.expander("🔥 Reset"):
    if st.text_input("Password",type="password")==PASSWORD and st.button("Wipe"):
        if os.path.exists(DATA): os.remove(DATA); ss.hist.clear(); st.warning("Reset!"); st.experimental_rerun()
