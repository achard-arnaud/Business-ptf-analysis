# Rédaction exec v0.3

**Contrat conditionnel.** Entrée : figures, claims, drivers, schéma et template exec v0.3. Sortie : payload narratif sourcé prêt pour validation/rendu. **Retour :** [composition.md](composition.md) pour le contrôle et la QA, puis [learning.md](learning.md). Contrat complet : [workflow.md](workflow.md).


Charger `templates/THREE_PAGER_EXEC_v0.3.md` pour les cadres et les prompts détaillés. Le profil est une projection du bundle : faits et calculs sourcés dans `figures`, inférences qualifiées dans les verbes, hypothèses conditionnelles. Aucun chiffre nouveau dans la conclusion.

1. Page 1 : signalétique et exposition économique, thèse écrite après le diagnostic, cinq drivers ordonnés, répartition d'activité, mandataires identifiés avec preuve et fonction manquante, SWOT et posture TOWS. Le pied introduit Core/Enabler/Support.
2. Page 2 : quatre activités de soutien et cinq principales de Porter, faits propres à l'entreprise, bénéfices et étoiles, renvoi de chaque ★★★ vers un thème ou la transformation. Sensibilités financières uniquement à partir de figures traçables ; ne pas les présenter comme ROI.
3. Page 3 : quadrant 3×3, trois à cinq programmes de priorité au format bénéfice/avantage/classe technique, transformation MT/LT, diagnostic public qualifié, stratégie dominante dérivée et conclusion reprenant la posture.

Chaque carte a un « À retenir » de jugement. Contrôler d'abord la traçabilité des faits, puis `render_exec.py`, `qa.py` et les trois PNG. Si la preuve manque, revenir à la recherche ; la QA de présentation ne la crée pas.

