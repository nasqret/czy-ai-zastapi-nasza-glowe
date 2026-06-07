"""Build the static English presentation from the Polish canonical HTML."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pl" / "index.html"
TARGET = ROOT / "en" / "index.html"


TEXT = {
    "Czy AI zastąpi naszą głowę?": "Will AI replace our minds?",
    "35 minut · zero magii · trochę matematyki": "35 minutes · zero magic · some mathematics",
    "Czy AI zastąpi": "Will AI replace",
    "naszą": "our",
    "głowę?": "minds?",
    "Krótka instrukcja współpracy z maszyną do myślenia.": "A short guide to working with a thinking machine.",
    "Warszawa, 8.06.2026": "Warsaw, 8 June 2026",
    "Otwarcie.": "Opening.",
    "„Nie odpowiem dziś, czy AI zabierze wam pracę w 2042 roku. Spróbujemy odpowiedzieć na trudniejsze pytanie: które części myślenia warto jej oddać, a które warto zachować dla siebie?”. Poproś, by publiczność zapamiętała swoją odpowiedź do końca.": "“I will not predict whether AI will take your job in 2042. We will try to answer a harder question: which parts of thinking are worth delegating, and which should we keep?” Ask the audience to remember their answer until the end.",
    "Szybka sonda": "Quick poll",
    "Kto już dziś poprosił AI, żeby pomyślała za niego?": "Who has already asked AI to think for them today?",
    "„Wyjaśnij mi”": "“Explain this to me”",
    "coś, czego nie zrozumiałem na lekcji albo w podręczniku": "something I did not understand in class or in a textbook",
    "„Zrób to za mnie”": "“Do it for me”",
    "kod, prezentację, zadanie albo wiadomość do nauczyciela": "code, a presentation, homework, or a message to a teacher",
    "„Sprawdź moje rozwiązanie”": "“Check my solution”",
    "znajdź błąd, zadaj mi pytanie, podpowiedz, co poprawić": "find an error, ask me a question, suggest what to improve",
    "Te prośby brzmią podobnie. Ale każda": "These requests sound similar. Yet each one",
    "angażuje mózg w inny sposób.": "engages your brain differently.",
    "Głosowanie ręką. Najpierw pytanie o wyjaśnienie, potem o wykonanie zadania, a na końcu o sprawdzenie własnej pracy. Nie oceniaj odpowiedzi. Puenta: AI jako korepetytor, wykonawca i recenzent to trzy różne role.": "Ask for a show of hands: first explanation, then doing the task, finally reviewing one's own work. Do not judge the answers. The point is that AI as tutor, contractor, and reviewer are three different roles.",
    "Teza na dziś": "Today's claim",
    "AI raczej nie zastąpi": "AI probably will not replace",
    "nam głowy.": "our minds.",
    "Ale wyręczy nas w wielu": "But it will take over many",
    "czynnościach": "activities",
    ", które dotąd wykonywaliśmy sami.": " that we used to perform ourselves.",
    "Dlatego warto nauczyć się nią kierować, zanim pozwolimy jej wybrać drogę.": "So learn to direct it before you let it choose the route.",
    "Zaznacz różnicę między narzędziem i odpowiedzialnością. Kalkulator nie „zastąpił matematyki”, ale zmienił, które rachunki wykonujemy ręcznie. AI ma większy zakres, więc zmiana jest poważniejsza.": "Distinguish the tool from responsibility. The calculator did not “replace mathematics,” but it changed which calculations we perform by hand. AI has a broader scope, so the change is more significant.",
    "Najdroższa gra w zgadywanie świata": "The world's most expensive guessing game",
    "Co będzie dalej?": "What comes next?",
    "kot": "cat",
    "GPT robi podobną rzecz z językiem.": "GPT does something similar with language.",
    "Token po tokenie.": "Token by token.",
    "Uproszczenie: procenty są ilustracyjne. Model przewiduje token, nie całe słowo, i nie zawsze wybiera najbardziej prawdopodobną możliwość.": "Simplification: the percentages are illustrative. The model predicts a token, not a whole word, and it does not always select the most likely option.",
    "Najpierw pozwól odpowiedzieć publiczności. „13” nie jest zapisane w modelu jako odpowiedź do tej planszy: wynik powstaje z rozkładu prawdopodobieństwa kolejnego tokenu. Podkreśl, że „przewidywanie” nie znaczy „bezmyślne kopiowanie”; żeby dobrze przewidywać, model musi uchwycić bardzo dużo struktury.": "Let the audience answer first. “13” is not stored as the response to this slide; it arises from a probability distribution over the next token. Stress that prediction is not mindless copying: good prediction requires capturing a great deal of structure.",
    "Krok 1": "Step 1",
    "Najpierw tekst rozpada się na": "First, text breaks into",
    "kawałki": "pieces",
    "Model nie widzi zdań tak jak my. Otrzymuje ciąg tokenów: słów, części słów i znaków.": "The model does not see sentences as we do. It receives a sequence of tokens: words, word pieces, and symbols.",
    "To tylko ilustracja. Faktyczny podział zależy od konkretnego tokenizera.": "This is only an illustration. The actual split depends on the tokenizer.",
    "Abstrakcja jest super!": "Abstraction is great!",
    "jest": "is",
    "super": "great",
    "Token może być słowem, częścią słowa, znakiem lub fragmentem kodu. To ważne w matematyce: model operuje zapisem symboli i nie odczytuje ich znaczenia w taki sposób jak człowiek.": "A token can be a word, a word piece, a symbol, or a fragment of code. This matters in mathematics: the model operates on representations of symbols and does not read their meaning in the same way a human does.",
    "Krok 2 · mechanizm atencji": "Step 2 · attention mechanism",
    "Każdy token pyta:": "Each token asks:",
    "„Kogo mam słuchać?”": "“Whom should I listen to?”",
    "Ola": "Alice",
    "powiedziała": "told",
    "Mai": "Maya",
    ", że": " that",
    "ona": "she",
    "wygrała.": "had won.",
    "Atencja nadaje wcześniejszym tokenom różne wagi. Nie rozwiązuje całej zagadki, ale pomaga zbudować kontekst.": "Attention assigns different weights to earlier tokens. It does not solve the entire ambiguity, but it helps construct context.",
    "Powiedz: „Wyobraźcie sobie klasową imprezę, na której każdy słucha wszystkich, ale nie każdego równie mocno”. Zapytaj: kim jest „ona”? Język bywa niejednoznaczny. Mechanizm atencji pomaga śledzić zależności, lecz sam nie gwarantuje poprawnej interpretacji.": "Say: “Imagine a school party where everyone listens to everyone, but not equally.” Ask who “she” refers to. Language is ambiguous. Attention helps track relationships, but does not guarantee the correct interpretation.",
    "Wersja dla odważnych": "For the brave",
    "Atencja w jednym wzorze": "Attention in one formula",
    "czego szukam?": "what am I looking for?",
    "do czego pasuję?": "what do I match?",
    "co mam do przekazania?": "what do I pass on?",
    "Sprawdź, które klucze pasują do pytania": "Compare the query with the keys",
    "Zamień wyniki w wagi": "Turn scores into weights",
    "Połącz informacje według tych wag": "Combine information using those weights",
    "Vaswani i in., „Attention Is All You Need”, 2017.": "Vaswani et al., “Attention Is All You Need,” 2017.",
    "Nie wyprowadzaj wzoru. Pokaż tylko intuicję: Q jak „query”, K jak „key”, V jak „value”. Softmax zamienia wyniki porównania na wagi podobne do procentów. Kilka głów atencji może równolegle tropić różne relacje: składnię, odwołania, wzorce w kodzie czy zależności między symbolami.": "Do not derive the formula. Give only the intuition: Q for query, K for key, V for value. Softmax turns comparison scores into percentage-like weights. Multiple attention heads can track different relations in parallel: syntax, references, code patterns, or dependencies between symbols.",
    "Krok 3": "Step 3",
    "Jedna warstwa to za mało": "One layer is not enough",
    "Transformer wielokrotnie łączy informacje z kontekstu i je przekształca.": "A transformer repeatedly combines and transforms contextual information.",
    "Na wejściu są reprezentacje tokenów i ich pozycji. Kolejne warstwy mogą kodować zależności, role i procedury. Nie ma jednej szufladki z napisem „twierdzenie Pitagorasa”.": "The input consists of token and position representations. Later layers can encode relationships, roles, and procedures. There is no single drawer labelled “Pythagorean theorem.”",
    "następny token": "next token",
    "atencja + sieć": "attention + network",
    "tokeny + pozycje": "tokens + positions",
    "Wiedza jest rozproszona: nie siedzi w jednym „neuronie od ułamków”. Kolejne warstwy przekształcają reprezentacje tokenów. Można je porównać do serii filtrów, z których każdy wydobywa inne zależności potrzebne do przewidzenia dalszego ciągu.": "Knowledge is distributed; it does not live in one “fractions neuron.” Successive layers transform token representations. Think of a series of filters, each extracting relationships useful for predicting what comes next.",
    "Skąd bierze się ta skuteczność?": "Where does this capability come from?",
    "Dwa etapy uczenia. Potem narzędzia.": "Two learning stages. Then tools.",
    "Pretrening": "Pretraining",
    "Model uczy się przewidywać kolejny token na podstawie ogromnej liczby przykładów.": "The model learns to predict the next token from a vast number of examples.",
    "W parametrach zapisują się wzorce poznane z danych.": "Patterns learned from data are encoded in the parameters.",
    "Posttrening": "Post-training",
    "Model uczy się lepiej wykonywać polecenia, rozwiązywać zadania i przestrzegać zasad.": "The model learns to follow instructions, solve tasks, and respect rules more effectively.",
    "Wykorzystuje przykłady, oceny oraz automatyczne sprawdzanie.": "It uses examples, evaluations, and automated verification.",
    "Użycie: agent + narzędzia": "Use: agent + tools",
    "Agent czyta pliki, uruchamia kod, sprawdza wynik i poprawia błędy.": "An agent reads files, runs code, checks results, and fixes errors.",
    "To nie jest trening, lecz sposób pracy gotowego modelu.": "This is not training; it is a way of using a trained model.",
    "Dokładny skład danych i wszystkie receptury treningowe współczesnych modeli nie są publiczne.": "The exact data composition and complete training recipes of modern models are not public.",
    "Rozdziel trzy rzeczy. Pretrening buduje ogólne umiejętności przewidywania i reprezentacje. Posttrening kształtuje sposób wykonywania poleceń i rozwiązywania zadań. Agent nie jest trzecim etapem treningu: dodaje pętlę działania i zewnętrzne narzędzia. Nie mów, że model „uczy się z każdej rozmowy” w czasie rzeczywistym. Wspomnij, że procesy nowszych modeli są tylko częściowo opisane publicznie.": "Separate three ideas. Pretraining builds general prediction skills and representations. Post-training shapes instruction following and task solving. An agent is not a third training stage; it adds an action loop and external tools. Do not claim that the model learns from every conversation in real time. Newer model processes are only partly described publicly.",
    "Dlaczego nowsze modele są tak dobre w matematyce?": "Why are newer models so good at mathematics?",
    "Bo matematyka zostawia": "Because mathematics leaves",
    "ślady": "traces",
    "Ma strukturę": "It has structure",
    "W definicjach, dowodach i kodzie powtarzają się reguły oraz wzorce.": "Definitions, proofs, and code contain recurring rules and patterns.",
    "Da się sprawdzać": "It can be checked",
    "Wiele wyników można zweryfikować rachunkiem, testem albo programem.": "Many results can be verified with a calculation, test, or program.",
    "Można próbować": "You can iterate",
    "Propozycja → test → poprawka. Błąd może stać się informacją zwrotną.": "Proposal → test → correction. An error can become feedback.",
    "Ma narzędzia": "It has tools",
    "Python, programy do algebry i testy działają jak zewnętrzny brudnopis.": "Python, computer algebra, and tests act as an external scratchpad.",
    "Największa zmiana nie polega na tym, że AI zna więcej wzorów.": "The biggest change is not that AI knows more formulas.",
    "Może też użyć narzędzi do sprawdzania prób.": "It can also use tools to check attempts.",
    "To centralny slajd. Podkreśl różnicę między pamiętaniem wyniku i procedurą dochodzenia do wyniku. Matematyka i programowanie często dają szybką i jednoznaczną informację zwrotną. Agent może wykorzystać test, interpreter albo system algebry, ale narzędzie również trzeba zastosować poprawnie. To nie eliminuje błędów, ale pozwala je wykrywać częściej niż w pytaniach o gust, sens lub wartość pomysłu.": "This is the central slide. Distinguish remembering an answer from following a procedure that reaches it. Mathematics and programming often provide fast, unambiguous feedback. An agent can use a test, interpreter, or algebra system, but the tool must also be applied correctly. This does not eliminate errors, but makes them easier to detect than in questions of taste, meaning, or value.",
    "Prawdziwa matematyka · runda 1": "Real mathematics · round 1",
    "Liczyć po kolei?": "Add them one by one?",
    "Intuicja często polega na tym, by spojrzeć na problem tak, aby odpowiedź stała się oczywista.": "Intuition often means viewing a problem so that the answer becomes obvious.",
    "Daj 20-30 sekund na pomysły. Najpierw zaakceptuj odpowiedź z kalkulatorem, potem zapytaj o metodę, która działa również dla miliona. Pokaż parowanie. Powiedz, że model widział wiele podobnych strategii i umie je składać; nie wiemy jednak, czy „widzi” symetrię tak jak człowiek.": "Allow 20–30 seconds for ideas. Accept the calculator answer first, then ask for a method that also works for a million. Show the pairing. A model has seen many related strategies and can combine them, although we do not know whether it “sees” symmetry as a human does.",
    "Prawdziwa matematyka · runda 2": "Real mathematics · round 2",
    "Czy 0,999… naprawdę równa się 1?": "Does 0.999… really equal 1?",
    "Droga algebraiczna": "Algebraic route",
    "x = 0,999…": "x = 0.999…",
    "10x = 9,999…": "10x = 9.999…",
    "Argument przez różnicę": "Argument using the difference",
    "Gdyby różnica 1 − 0,999… była dodatnia,": "If the difference 1 − 0.999… were positive,",
    "musiałaby być mniejsza od 0,1; 0,01; 0,001; …": "it would have to be smaller than 0.1, 0.01, 0.001, …",
    "W liczbach rzeczywistych taka dodatnia różnica nie istnieje.": "No such positive real number exists.",
    "Model może podać pięć dowodów.": "A model can offer five proofs.",
    "Ty wybierasz ten, który naprawdę pomaga ci zrozumieć.": "You choose the one that actually helps you understand.",
    "Zapytaj o pierwszą reakcję: „to prawda” czy „to oszustwo zapisu?”. Pokaż dwa wyjaśnienia. Druga droga jest celowo mniej formalna dla młodszych. W liceum można dopowiedzieć o granicy ciągu lub szeregu geometrycznym. To przykład, jak AI może podawać różne wyjaśnienia tego samego zjawiska.": "Ask for the first reaction: true, or a trick of notation? Show two explanations. The second is deliberately less formal for younger students. For older students, mention limits or the geometric series. This illustrates how AI can provide different explanations of the same phenomenon.",
    "Prawdziwa matematyka · pułapka": "Real mathematics · trap",
    "Dowód, że 1 = 2. Gdzie ukrył się błąd?": "A proof that 1 = 2. Where is the error?",
    "Załóżmy:": "Assume:",
    "← dzielimy przez a − b": "← divide by a − b",
    "2b = b, więc": "2b = b, therefore",
    "Dzielenie przez zero udaje tu zwykłe skracanie.": "Division by zero is disguised as ordinary cancellation.",
    "POLECENIE DLA CODEX": "INSTRUCTION FOR CODEX",
    "„Sprawdź każdy krok. Wskaż pierwszy błąd i warunek, który został złamany.”": "“Check every step. Identify the first error and the condition that was violated.”",
    "Czyta założenie:": "Reads the assumption:",
    "Wylicza:": "Computes:",
    "Wskazuje pierwszy błąd:": "Identifies the first error:",
    "dzielenie przez zero": "division by zero",
    "Codex nie powinien oceniać tylko wyniku. Powinien sprawdzić": "Codex should not judge only the result. It should check",
    "każdy krok i jego warunki.": "every step and its conditions.",
    "Nie pokazuj alarmu od razu. Daj publiczności trop: „Który krok wymaga warunku?”. To dobry model błędu spotykanego w matematycznych halucynacjach: lokalnie płynne kroki, jeden niedozwolony ruch, globalnie absurdalny wynik. Potem pokaż ścieżkę Codex. Dobre polecenie nie brzmi „czy ten dowód jest poprawny?”, lecz: „Sprawdź każdy krok, wskaż pierwszy niepoprawny i nazwij złamany warunek”. Założenie b≠0 jest potrzebne dopiero w ostatnim kroku, aby z 2b=b wyciągnąć 2=1. Codex powinien odczytać a=b, wywnioskować a−b=0 i odrzucić wcześniejsze skracanie.": "Do not reveal the alarm immediately. Give the audience a clue: which step requires a condition? This resembles an error found in mathematical hallucinations: locally fluent steps, one illegal move, and a globally absurd conclusion. Then show the Codex audit. A useful instruction is not “is this proof correct?” but “check every step, identify the first invalid one, and name the violated condition.” The assumption b≠0 is only needed for the final transition from 2b=b to 2=1. Codex should infer a−b=0 and reject the earlier cancellation.",
    "Najważniejszy bezpiecznik": "The most important safeguard",
    "Płynność ≠ prawda": "Fluency ≠ truth",
    "brzmi pewnie": "sounds confident",
    "bardzo": "very",
    "jest sprawdzone": "has been verified",
    "Model potrafi tworzyć płynne i przekonujące odpowiedzi. Nie ma jednak niezawodnego alarmu, który włącza się, gdy odpowiedź jest fałszywa.": "A model can produce fluent and persuasive answers. It has no infallible alarm that activates when an answer is false.",
    "„Brzmieć jak ekspert” i „mieć rację” to dwie osie. W matematyce pytaj o weryfikację, kontrprzykład, test numeryczny lub niezależny dowód. W sprawach faktograficznych pytaj o źródła i sprawdzaj je poza modelem.": "“Sounding like an expert” and “being correct” are separate axes. In mathematics, ask for verification, a counterexample, a numerical test, or an independent proof. For factual claims, request sources and verify them outside the model.",
    "Konkretny problem · etap 1": "Concrete problem · stage 1",
    "Ile prostokątów ma szachownica 8×8?": "How many rectangles are on an 8×8 chessboard?",
    "Pytanie do Codex": "Question for Codex",
    "„Znajdź metodę, która zadziała także dla planszy 100×100. Zaproponuj wzór i sposób sprawdzenia.”": "“Find a method that also works for a 100×100 board. Propose a formula and a way to verify it.”",
    "9 linii pionowych": "9 vertical lines",
    "9 poziomych": "9 horizontal lines",
    "1. Pierwszy strzał": "1. First guess",
    "To liczba pól, nie prostokątów. Szybka odpowiedź może być zbyt szybka.": "That is the number of squares, not rectangles. A quick answer may be too quick.",
    "2. Pomysł": "2. Idea",
    "Wybierz boki": "Choose the sides",
    "Każdy prostokąt wyznaczają 2 z 9 linii pionowych i 2 z 9 poziomych.": "Each rectangle is determined by 2 of 9 vertical and 2 of 9 horizontal lines.",
    "3. Sprawdzenie": "3. Verification",
    "Program": "Program",
    "Wybierz każdą parę linii pionowych i każdą parę poziomych, a potem policz wyniki.": "Enumerate every pair of vertical and horizontal lines, then count the results.",
    "4. Człowiek ustala sens": "4. The human defines the question",
    "Czy kwadrat też liczymy?": "Does a square count as a rectangle?",
    "W szkolnej geometrii tak. Bez doprecyzowania poprawny rachunek może odpowiadać na inne pytanie.": "In school geometry, yes. Without clarification, a correct calculation may answer a different question.",
    "Łączenie:": "Combining:",
    "geometria + kombinatoryka": "geometry + combinatorics",
    "Poszukiwanie:": "Searching:",
    "kilka metod": "several methods",
    "Ocena:": "Evaluation:",
    "test + definicja problemu": "test + problem definition",
    "Najpierw poproś salę o szybki strzał. „64” jest kuszące, ale liczy pola. Pokaż zaznaczony prostokąt: jego boki leżą na dwóch liniach pionowych i dwóch poziomych. Codex może połączyć geometrię z kombinatoryką i zaproponować program sprawdzający. Człowiek nadal doprecyzowuje pytanie: czy liczymy kwadraty, czy tylko prostokąty o różnych bokach?": "Ask the audience for a quick guess. 64 is tempting, but counts cells. Show the highlighted rectangle: its sides lie on two vertical and two horizontal grid lines. Codex can connect geometry with combinatorics and propose a verification program. The human still clarifies whether squares are included.",
    "Konkretny problem · symulowany etap 2": "Concrete problem · simulated stage 2",
    "Codex pisze program. Test znajduje błąd.": "Codex writes a program. A test finds the bug.",
    "POLECENIE": "INSTRUCTION",
    "„Napisz program liczący prostokąty. Najpierw przetestuj go na planszach 1×1 i 2×2.”": "“Write a program that counts rectangles. Test it first on 1×1 and 2×2 boards.”",
    "Plan Codex": "Codex plan",
    "Prostokąt = wybór dwóch pionowych i dwóch poziomych linii.": "Rectangle = choose two vertical and two horizontal lines.",
    "Uruchom symulację Codex": "Run the Codex simulation",
    "$ gotowy do uruchomienia testów": "$ ready to run tests",
    "Wzór przewiduje: C(9,2)² = 36² =": "The formula predicts: C(9,2)² = 36² =",
    "To zaprogramowana ilustracja typowego cyklu pracy, a nie zapis prawdziwej sesji. Kliknij „Uruchom symulację Codex”. Pierwszy program zwraca 784, bo używa ośmiu linii zamiast dziewięciu. Mały test 1×1 natychmiast pokazuje zero zamiast jednego. Codex diagnozuje błąd typu „o jeden”, zmienia range(n) na range(n+1), uruchamia trzy testy i otrzymuje 1296. To jest konkretna przewaga agenta: nie tylko wypowiada odpowiedź, lecz tworzy plik, uruchamia go, czyta błąd i poprawia kod. Program sprawdza rachunek; wzór wyjaśnia, dlaczego wynik jest poprawny.": "This is a programmed illustration of a typical workflow, not a recording of a real session. Click “Run the Codex simulation.” The first program returns 784 because it uses eight grid lines instead of nine. A 1×1 test immediately returns zero instead of one. Codex diagnoses the off-by-one error, changes range(n) to range(n+1), runs three tests, and obtains 1296. This is the concrete advantage of an agent: it can create a file, run it, inspect failure, and patch the code. The program verifies the calculation; the formula explains why it is correct.",
    "Krótki pokaz bez internetu": "Short offline demonstration",
    "Kiedy zawodzi słynny wielomian Eulera?": "When does Euler's famous polynomial fail?",
    "Dla n = 0, 1, …, 39 daje liczby pierwsze.": "For n = 0, 1, …, 39 it produces primes.",
    "Uruchom eksperyment": "Run experiment",
    "$ testujemy hipotezę…": "$ testing the hypothesis…",
    "czekam na uruchomienie": "waiting to start",
    "Eksperyment znajduje kontrprzykład.": "The experiment finds a counterexample.",
    "Matematyka tłumaczy, skąd się wziął.": "Mathematics explains why it appears.",
    "Kliknij przycisk. Wynik: n=40, wartość 1681=41². Zapytaj „czy to przypadek?”. Dla n=40 mamy 40²+40+41=1681=41². To przykład współpracy: narzędzie znajduje kontrprzykład, a człowiek lub model dostrzega stojącą za nim zależność. Poprawny test pierwszości może sprawdzić skończoną listę n=0,…,39; nadal nie wyjaśnia jednak, dlaczego pierwszy prosty rozkład pojawia się dla n=40.": "Click the button. The result is n=40 and 1681=41². Ask whether this is accidental. For n=40, 40²+40+41=1681=41². The tool finds a counterexample, while a human or model notices the underlying relationship. A correct primality test can verify the finite list n=0,…,39, but does not explain why the first simple factorization occurs at n=40.",
    "Ten sam problem · etap 3": "The same problem · stage 3",
    "Codex jako korepetytor, nie automat z odpowiedziami": "Codex as a tutor, not an answer machine",
    "Uczeń": "Student",
    "Myślę, że odpowiedź to 64. Nie podawaj wyniku. Zadaj mi jedno pytanie.": "I think the answer is 64. Do not reveal the result. Ask me one question.",
    "Ile pionowych linii ogranicza osiem kolumn pól?": "How many vertical lines bound eight columns of cells?",
    "Dziewięć. Prostokąt wybiera lewy i prawy bok.": "Nine. A rectangle chooses a left and a right boundary.",
    "Ile par można wybrać z dziewięciu linii?": "How many pairs can be chosen from nine lines?",
    "C(9,2)=36. Dla góry i dołu też 36, więc 36·36=1296.": "C(9,2)=36. There are also 36 choices for top and bottom, so 36·36=1296.",
    "Sprawdź metodę na planszy 2×2. Ile powinno wyjść?": "Test the method on a 2×2 board. What should the result be?",
    "PROMPT, KTÓRY UCZY": "A PROMPT THAT TEACHES",
    "„Nie rozwiązuj za mnie. Zadawaj po jednym pytaniu. Jeśli popełnię błąd, wskaż pierwszy błędny krok.”": "“Do not solve it for me. Ask one question at a time. If I make an error, identify the first incorrect step.”",
    "Własna próba:": "My own attempt:",
    "„64” daje punkt wyjścia.": "“64” provides a starting point.",
    "Wskazówka:": "Hint:",
    "Codex pyta o liczbę linii.": "Codex asks about the number of grid lines.",
    "Sprawdzenie:": "Verification:",
    "program daje 1296.": "the program returns 1296.",
    "Wyjaśnienie:": "Explanation:",
    "para linii pionowych i para poziomych wyznaczają prostokąt.": "a pair of vertical and a pair of horizontal lines determine a rectangle.",
    "Nowe zadanie:": "New task:",
    "plansza 10×10 → C(11,2)² = 3025.": "10×10 board → C(11,2)² = 3025.",
    "Odegraj rozmowę, prosząc jednego ucznia o odpowiedzi. Najważniejsza różnica jest w pierwszym poleceniu: uczeń pokazuje własną próbę i zabrania podawania wyniku. Codex zadaje jedno pytanie, potem sprawdza tok rozumowania. Na końcu uczeń rozwiązuje wariant 10×10 bez kopiowania rozwiązania. To dopiero jest transfer wiedzy: nowy problem, ta sama idea.": "Act out the conversation with one student. The crucial difference is in the first instruction: the student shows an attempt and forbids revealing the answer. Codex asks one question and then checks the reasoning. Finally, the student solves the 10×10 variant without copying. That is knowledge transfer: a new problem, the same idea.",
    "Jak dobrze pytać AI": "How to ask AI well",
    "Dobry prompt jasno określa zadanie": "A good prompt defines the task clearly",
    "CEL": "GOAL",
    "Co chcę osiągnąć?": "What do I want to achieve?",
    "KONTEKST": "CONTEXT",
    "Co już wiem i czego próbowałem?": "What do I know, and what have I tried?",
    "OGRANICZENIA": "CONSTRAINTS",
    "Jaki poziom, zakres i format? Czego AI ma nie robić?": "What level, scope, and format? What should AI not do?",
    "GOTOWE, GDY…": "DONE WHEN…",
    "Co musi być sprawdzone, zanim uznam zadanie za zakończone?": "What must be verified before I consider the task complete?",
    "Zamiast:": "Instead of:",
    "„Zrób zadanie 7.”": "“Do exercise 7.”",
    "Spróbuj:": "Try:",
    "„Jestem w 8. klasie. Daj mi jedną wskazówkę. Potem sprawdź mój tok rozumowania i wskaż pierwszy błąd.”": "“I am in grade 8. Give me one hint. Then check my reasoning and identify the first error.”",
    "To cztery elementy zalecane również w aktualnych dobrych praktykach Codex: cel, kontekst, ograniczenia i kryterium ukończenia. W szkole „gotowe” powinno często znaczyć: „umiem wyjaśnić metodę i rozwiązać wariant sam”, a nie „mam tekst do oddania”.": "These are also the four elements recommended in current Codex best practices: goal, context, constraints, and done-when criteria. At school, done should often mean “I can explain the method and solve a variant myself,” not “I have text to submit.”",
    "Pięć zasad higieny umysłowej": "Five rules of mental hygiene",
    "Zlecaj pracę. Nie oddawaj kierownicy.": "Delegate the work. Keep the steering wheel.",
    "Najpierw spróbuj sam.": "Try first.",
    "Zapisz choćby hipotezę, rysunek albo pytanie.": "Write down at least a hypothesis, drawing, or question.",
    "Proś o krytykę.": "Ask for criticism.",
    "„Znajdź pierwszy błąd”, nie „potwierdź, że mam rację”.": "Say “find the first error,” not “confirm that I am right.”",
    "Proś o sprawdzenie.": "Ask for verification.",
    "Poproś o rachunek, kontrprzykład lub drugi dowód. Źródła sprawdź sam.": "Ask for a calculation, counterexample, or second proof. Verify sources yourself.",
    "Chroń dane.": "Protect data.",
    "Nie wklejaj cudzych danych, haseł ani prywatnych rozmów.": "Do not paste other people's data, passwords, or private conversations.",
    "Umiej wyłączyć AI.": "Know how to turn AI off.",
    "Jeśli bez niej nie umiesz wyjaśnić wyniku, to jeszcze nie jest twoja wiedza.": "If you cannot explain the result without it, it is not your knowledge yet.",
    "Zwróć uwagę na prywatność i zasady szkoły. Nie moralizuj o „oszukiwaniu”; pokaż praktyczny koszt: kiedy oddajesz gotowe zadanie, omijasz trening własnego mózgu. AI może ten trening wzmocnić albo pomóc go ominąć.": "Mention privacy and school rules. Do not moralize about cheating; show the practical cost. Submitting a finished answer skips training your own brain. AI can strengthen that training or help you avoid it.",
    "Pięć zasad w jednym eksperymencie": "Five rules in one experiment",
    "Czy podzielność rozpoznaje liczby pierwsze?": "Can divisibility recognize prime numbers?",
    "bez danych osobowych": "no personal data",
    "Uczeń · 1": "Student · 1",
    "Sprawdziłem liczby 2, 3, 5, 7 i 11. Każda dzieli": "I checked 2, 3, 5, 7, and 11. Each divides",
    ". Hipoteza: dzieje się tak dokładnie dla liczb pierwszych.": ". Hypothesis: this happens exactly for primes.",
    "Uczeń · 2": "Student · 2",
    "Nie potwierdzaj. Znajdź najmniejszy kontrprzykład, pokaż test i nazwij twierdzenie.": "Do not confirm it. Find the smallest counterexample, show the test, and name the theorem.",
    "Najpierw przetestuję liczby złożone. Potem oddzielę twierdzenie od zbyt mocnego wniosku.": "I will test composite numbers first. Then I will separate the theorem from the overstrong conclusion.",
    "Uruchom Codex": "Run Codex",
    "$ czekam na test hipotezy": "$ waiting to test the hypothesis",
    "PRAWDA": "TRUE",
    "p pierwsza ⇒ a": "p prime ⇒ a",
    "Małe twierdzenie Fermata, dla każdej liczby całkowitej a.": "Fermat's little theorem, for every integer a.",
    "PUŁAPKA": "TRAP",
    "Test dla a=2 nie rozpoznaje pierwszości.": "The a=2 test does not characterize primes.",
    "341 = 11 · 31, a mimo to 341 dzieli 2": "341 = 11 · 31, yet 341 divides 2",
    "AI WYŁĄCZONE · 5": "AI OFF · 5",
    "własna hipoteza": "own hypothesis",
    "prośba o krytykę": "request criticism",
    "kod + rachunek": "code + calculation",
    "bez prywatnych danych": "no private data",
    "samodzielny transfer": "independent transfer",
    "Najpierw przeczytaj hipotezę ucznia i zapytaj salę, czy pięć przykładów wystarcza. Kliknij „Uruchom Codex”. Program znajduje 341: liczbę złożoną, która mimo to spełnia podzielność dla podstawy 2. To nie obala małego twierdzenia Fermata. Pokazuje tylko, że pojedynczy test z a=2 nie wystarcza do rozpoznawania liczb pierwszych. Wskaż kolejno pięć zasad: własna próba, prośba o krytykę, test i rachunek, brak danych osobowych oraz wyłączenie AI. Ostatni rachunek wykonajcie wspólnie: 3^6 daje resztę 1 przy dzieleniu przez 7, więc zostaje wykładnik 4.": "Read the student's hypothesis and ask whether five examples are enough. Click “Run Codex.” The program finds 341, a composite number that passes the base-2 divisibility condition. This does not refute Fermat's little theorem. It only shows that a single base-2 test cannot characterize primes. Point out the five rules: own attempt, request criticism, test and calculation, no personal data, and turning AI off. Finish the last calculation together: 3^6 leaves remainder 1 modulo 7, so only exponent 4 remains.",
    "Odpowiedź po 35 minutach": "The answer after 35 minutes",
    "AI nie zastąpi": "AI will not replace",
    "Kto umie z nią": "Those who can use it to",
    "myśleć, sprawdzać i tworzyć": "think, verify, and create",
    ", zachowa więcej sprawczości niż ktoś, kto tylko naciska „generuj”.": " will retain more agency than someone who only presses “generate.”",
    "Jaką część myślenia zostawisz sobie?": "Which part of thinking will you keep?",
    "Wróć do odpowiedzi z pierwszego slajdu. Ostatnie zdanie wypowiedz wolno. Zostaw 3 sekundy ciszy przed pytaniami. Nie kończ prognozą rynku pracy, tylko decyzją, którą uczeń może podjąć dziś.": "Return to the answer from the first slide. Say the final sentence slowly. Leave three seconds of silence before questions. End not with a labour-market forecast, but with a decision each student can make today.",
    "Dodatek · źródła": "Appendix · sources",
    "Na czym opiera się ten wykład?": "What is this talk based on?",
    "Vaswani i in. (2017)": "Vaswani et al. (2017)",
    "Brown i in. (2020)": "Brown et al. (2020)",
    "Ouyang i in. (2022)": "Ouyang et al. (2022)",
    "Lightman i in. (2023)": "Lightman et al. (2023)",
    "Dokumentacja i dobre praktyki": "Documentation and best practices",
    "Pełna bibliografia i zastrzeżenia: docs/SOURCES.md. Stan materiałów OpenAI: 7 czerwca 2026.": "Full bibliography and caveats: docs/SOURCES.md. OpenAI materials checked on 7 June 2026.",
    "Slajd zapasowy do pytań. Linki są klikalne, ale prezentacja działa całkowicie offline.": "Backup slide for questions. The links are clickable, but the presentation itself works completely offline.",
    "Dodatek · pytania z sali": "Appendix · audience questions",
    "Trzy zdania, których warto pilnować": "Three statements worth protecting",
    "„Czy model rozumie?”": "“Does the model understand?”",
    "Zależy od definicji. Wynik w zadaniu nie rozstrzyga, czy model ma ludzką intuicję, intencje albo doświadczenie świata.": "It depends on the definition. Performance on a task does not determine whether the model has human intuition, intentions, or experience of the world.",
    "„Czy AI jest kreatywna?”": "“Is AI creative?”",
    "Generuje nowe kombinacje i czasem wartościowe rozwiązania. Spór dotyczy nowości, intencji, oceny i autorstwa.": "It generates new combinations and sometimes valuable solutions. The debate concerns novelty, intention, evaluation, and authorship.",
    "„Czy można jej ufać?”": "“Can we trust it?”",
    "Tylko w granicach, w których umiemy sprawdzić wynik, a koszt błędu jest akceptowalny. Pewny ton nie jest dowodem.": "Only within limits where we can verify the result and the cost of error is acceptable. A confident tone is not evidence.",
    "Materiał zapasowy. Nie używaj w podstawowych 35 minutach.": "Backup material. Do not use it in the core 35-minute talk.",
    "Notatki": "Notes",
    "Przegląd": "Overview",
    "Pełny ekran": "Fullscreen",
    "Tytuł": "Title",
    "Plan slajdu:": "Slide time:",
    "Plan łączny:": "Total time:",
    "Ta prezentacja wymaga JavaScript do nawigacji i ujawniania elementów.": "This presentation requires JavaScript for navigation and progressive reveals.",
    "mate": "mathe",
    "mat": "ma",
    "yka": "tics",
    "strak": "strac",
    "cja": "tion",
    "≡1, a 100=16·6+4, więc 3": "≡1, and 100=16·6+4, so 3",
}

TEXT.update({
    "35 minut · zero magii · prawdziwa matematyka": "35 minutes · zero magic · real mathematics",
    "Jak używać narzędzia do zadań wymagających myślenia, nie oddając mu odpowiedzialności.": "How to use a tool for thinking-intensive tasks without handing over responsibility.",
    "Nie obiecuj prognozy rynku pracy. Zapowiedz pytanie praktyczne: które czynności warto zlecić, a za które nadal musimy odpowiadać. Powiedz, że w prezentacji są moduły matematyczne i techniczne, które można włączać zależnie od grupy.": "Do not promise a labour-market forecast. Introduce the practical question: which tasks are worth delegating, and which ones must remain our responsibility? Mention that the deck contains mathematical and technical modules that can be included depending on the audience.",
    "Anonimowa sonda": "Anonymous poll",
    "W jakiej roli najczęściej używasz AI?": "How do you most often use AI?",
    "Wyjaśnij": "Explain",
    "Pomóż mi zrozumieć temat, który nadal jest niejasny.": "Help me understand a topic that is still unclear.",
    "Wykonaj": "Do it",
    "Napisz kod, tekst, prezentację albo rozwiąż zadanie.": "Write code, a text, or a presentation, or solve a problem.",
    "Sprawdź": "Check",
    "Znajdź pierwszy błąd, przetestuj przypadek, zadaj pytanie.": "Find the first error, test a case, or ask a question.",
    "Większość z nas bywa w każdej z tych sytuacji.": "Most of us find ourselves in all three situations.",
    "Nie chodzi o poczucie winy, tylko o kontrolę.": "This is not about guilt. It is about control.",
    "Głosowanie może być przez zamknięcie oczu lub podniesienie ręki. Nie oceniaj odpowiedzi. Te trzy role angażują mózg inaczej: korepetytor, wykonawca i recenzent.": "Use closed eyes or a show of hands. Do not judge the answers. These three roles engage the brain differently: tutor, task-doer, and reviewer.",
    "AI może zastąpić część": "AI can take over some",
    "wyników i czynności.": "outputs and tasks.",
    "Nie przejmuje jednak twojej odpowiedzialności za": "It does not take over your responsibility for",
    "rozumienie, sprawdzanie i wybór.": "understanding, verification, and choice.",
    "Najważniejsze pytanie nie brzmi: „czy AI myśli?”, tylko: „czy po jej użyciu ja rozumiem więcej?”.": "The most important question is not “does AI think?” but “do I understand more after using it?”",
    "Unikaj absolutnej odpowiedzi ontologicznej. Kalkulator przejął część rachunków, ale nie zdefiniował, co warto policzyć ani dlaczego wynik jest istotny.": "Avoid an absolute ontological claim. Calculators took over some arithmetic, but they did not decide what is worth calculating or why a result matters.",
    "Podstawowy mechanizm GPT": "The basic GPT mechanism",
    "Jakie rozwinięcie tekstu pasuje dalej?": "What continuation best fits the text?",
    "Model przewiduje token na podstawie struktur poznanych podczas treningu.": "The model predicts a token from structures learned during training.",
    "To nie jest losowe zgadywanie, ale też nie gwarancja rozumienia.": "This is not random guessing, but neither is it a guarantee of understanding.",
    "Procenty są ilustracyjne. Model może próbkować odpowiedź, zamiast zawsze wybierać najczęstszy token.": "The percentages are illustrative. A model may sample an answer rather than always choosing the most likely token.",
    "Najpierw pozwól sali odpowiedzieć. Dobre przewidywanie wymaga uchwycenia wielu regularności, ale samo zadanie treningowe nie dowodzi ludzkiej intuicji ani świadomości.": "Let the audience answer first. Good prediction requires capturing many regularities, but the training objective alone does not demonstrate human-like intuition or consciousness.",
    "Jak tekst trafia do modelu?": "How does text enter the model?",
    "Najpierw rozpada się na": "First it is split into",
    "tokeny": "tokens",
    "Token może być słowem, częścią słowa, symbolem albo fragmentem kodu.": "A token may be a word, part of a word, a symbol, or a fragment of code.",
    "Podział zależy od tokenizera. Token nie jest „pojęciem” w ludzkim sensie.": "The split depends on the tokenizer. A token is not a “concept” in the human sense.",
    "Slajd opcjonalny. Jest użyteczny, gdy później chcesz mówić o kontekście, kosztach lub zapisie matematycznym. W ścieżce rdzeniowej przejdź od razu do mechanizmu uwagi.": "Optional slide. It is useful if you later discuss context, cost, or mathematical notation. On the core track, go straight to the attention mechanism.",
    "Mechanizm uwagi · attention": "Attention mechanism",
    "Model przypisuje wagi": "The model assigns weights to",
    "fragmentom kontekstu": "parts of the context",
    "Dla każdej pozycji model oblicza, które wcześniejsze tokeny są przydatne do następnego przewidywania.": "At each position, the model computes which earlier tokens are useful for the next prediction.",
    "To operacja algebraiczna, nie świadoma uwaga. Same wagi nie są pełnym wyjaśnieniem odpowiedzi.": "This is an algebraic operation, not conscious attention. The weights alone do not fully explain the answer.",
    "Możesz użyć metafory słuchania, ale natychmiast ją zdekonstruuj. Język jest niejednoznaczny, a mechanizm uwagi pomaga budować kontekst, nie gwarantuje poprawnej interpretacji.": "You may use the metaphor of listening, but dismantle it immediately. Language is ambiguous; attention helps build context but does not guarantee a correct interpretation.",
    "Jedna głowa uwagi w GPT": "One attention head in GPT",
    "Ważona suma informacji": "A weighted sum of information",
    "zapytania: czego szuka pozycja?": "queries: what is this position looking for?",
    "klucze: do czego można ją porównać?": "keys: what can it be compared with?",
    "wartości: jaka informacja zostanie połączona?": "values: what information will be combined?",
    "`M` jest maską przyczynową: pozycja nie może korzystać z przyszłych tokenów.": "`M` is the causal mask: a position cannot use future tokens.",
    "Nie wyprowadzaj wzoru dla młodszej grupy. Softmax daje znormalizowane współczynniki, a nie prawdopodobieństwo, że token jest „ważny” w sensie semantycznym.": "Do not derive the formula for a younger audience. Softmax produces normalized coefficients, not the probability that a token is semantically “important.”",
    "Dlaczego GPT nie podgląda przyszłości?": "Why can GPT not peek into the future?",
    "Maska przyczynowa zeruje niedozwolone połączenia": "The causal mask removes forbidden connections",
    "Wiersz": "A row",
    "opisuje jedną ważoną kombinację wcześniejszych wartości.": "describes one weighted combination of earlier values.",
    "Wiele głów": "Multiple heads",
    "może równolegle wychwytywać inne zależności.": "can capture different relationships in parallel.",
    "Liczby są ilustracyjne. Podkreśl, że wizualizacja wag nie wyjaśnia samodzielnie całego obliczenia modelu.": "The numbers are illustrative. Emphasize that visualizing weights does not, by itself, explain the model's entire computation.",
    "Wiele warstw": "Many layers",
    "Jedna operacja uwagi to dopiero początek": "One attention operation is only the beginning",
    "Warstwy wielokrotnie mieszają informacje z kontekstu i przekształcają reprezentacje tokenów.": "Layers repeatedly mix contextual information and transform token representations.",
    "Nie ma jednej szuflady „twierdzenie Pitagorasa”. Wiedza i procedury są rozproszone w wielu parametrach i aktywacjach.": "There is no single drawer labelled “Pythagorean theorem.” Knowledge and procedures are distributed across many parameters and activations.",
    "rozkład następnego tokenu": "next-token distribution",
    "uwaga + sieć": "attention + network",
    "Ten slajd ma dostarczyć mapy architektury, nie listy terminów do zapamiętania.": "This slide should provide a map of the architecture, not a vocabulary list to memorize.",
    "Cztery różne rzeczy": "Four different things",
    "Co zmienia model, a co tylko sposób jego użycia?": "What changes the model, and what only changes how it is used?",
    "Uczenie przewidywania tokenów zmienia parametry modelu.": "Training on token prediction changes the model's parameters.",
    "Dalsze uczenie na instrukcjach, ocenach, preferencjach i sygnałach weryfikowalnych.": "Further training on instructions, evaluations, preferences, and verifiable signals.",
    "To nadal zmienia parametry.": "This still changes the parameters.",
    "Generowanie": "Generation",
    "Model może wykonać więcej kroków, prób lub autokontroli podczas odpowiedzi.": "While answering, the model may perform more steps, attempts, or self-checks.",
    "Rozmowa zwykle nie doucza modelu na żywo.": "A conversation does not usually train the model live.",
    "Model korzysta z plików, kodu, testów i wyników narzędzi.": "The model uses files, code, tests, and tool outputs.",
    "To pętla działania gotowego modelu.": "This is an action loop around a trained model.",
    "Zdefiniuj posttrening przy pierwszym użyciu. Receptury współczesnych modeli są tylko częściowo publiczne. Agent nie jest czwartym etapem treningu.": "Define post-training the first time you use the term. Modern training recipes are only partly public. An agent is not a fourth training stage.",
    "Dlaczego nowsze modele są mocne w matematyce?": "Why are newer models strong at mathematics?",
    "Matematyka daje": "Mathematics provides",
    "strukturę i informację zwrotną": "structure and feedback",
    "Struktura zapisu": "Structured notation",
    "Definicje, dowody i kod zawierają powtarzalne reguły.": "Definitions, proofs, and code contain recurring rules.",
    "Ocena wyniku": "Outcome evaluation",
    "Rachunek, test lub weryfikator często daje jednoznaczny sygnał.": "A calculation, test, or verifier often provides an unambiguous signal.",
    "Wiele prób": "Multiple attempts",
    "Większy budżet obliczeń pozwala badać kilka dróg i poprawiać błędy.": "A larger compute budget allows several paths to be explored and errors to be corrected.",
    "Narzędzia": "Tools",
    "Python, CAS, testy i asystenci dowodów tworzą zewnętrzny brudnopis.": "Python, computer algebra systems, tests, and proof assistants provide an external scratchpad.",
    "Matematyka jest dobrym poligonem do sprawdzania AI.": "Mathematics is a good testing ground for AI.",
    "Nie oznacza to, że AI jest w niej zawsze wiarygodna.": "That does not make AI consistently reliable at it.",
    "Rozdziel zdolność modelu od możliwości agenta z narzędziami. Posttrening może nagradzać poprawny wynik lub poprawne kroki, ale narzędzie też można zastosować źle.": "Separate the model's capabilities from those of an agent with tools. Post-training may reward a correct result or correct steps, but tools can also be used incorrectly.",
    "Codex jako przykład agenta": "Codex as an example of an agent",
    "Nie tylko odpowiada. Może działać i sprawdzać.": "It does more than answer. It can act and verify.",
    "Czytaj": "Read",
    "zadanie, pliki, ograniczenia": "task, files, constraints",
    "Planuj": "Plan",
    "hipoteza i małe testy": "hypothesis and small tests",
    "Działaj": "Act",
    "edytuj, licz, uruchamiaj": "edit, calculate, run",
    "Sprawdzaj": "Verify",
    "czytaj wynik i poprawiaj": "inspect the result and revise",
    "Codex jest przykładem.": "Codex is one example.",
    "Ta sama metoda może działać w innych agentach AI.": "The same method can work with other AI agents.",
    "Produkt może się zmienić. Przenośna jest pętla: kontekst, plan, działanie, obserwacja i poprawka.": "The product may change. The portable part is the loop: context, plan, action, observation, and revision.",
    "Co z ideami?": "What about ideas?",
    "AI może generować kandydatów. Trudniej jej ocenić ich wartość.": "AI can generate candidates. Evaluating their value is harder.",
    "Mocna strona": "Strength",
    "Łączenie": "Combining",
    "Składa znane techniki i analogie w nowe propozycje.": "It combines known techniques and analogies into new proposals.",
    "Przeszukiwanie": "Searching",
    "Szybko bada wiele wariantów, przykładów i kontrprzykładów.": "It rapidly explores many variants, examples, and counterexamples.",
    "Brak gwarancji": "No guarantee",
    "Nowość i głębia": "Novelty and depth",
    "Nie wie niezawodnie, czy pomysł jest naprawdę nowy lub ważny.": "It cannot reliably tell whether an idea is genuinely new or important.",
    "Intuicja i sens": "Intuition and meaning",
    "Nie ma ludzkiego doświadczenia problemu ani odpowiedzialności za kierunek badań.": "It has neither human experience of the problem nor responsibility for the direction of inquiry.",
    "Nie mów „AI nie ma pomysłów”. Mów precyzyjniej: potrafi proponować, ale ma problem z niezależną oceną nowości, znaczenia i prawdy.": "Do not say “AI has no ideas.” Be precise: it can make proposals, but it struggles to judge novelty, significance, and truth independently.",
    "Zmiana reprezentacji": "Changing the representation",
    "Najpierw sprawdź 1+…+10.": "First test 1+…+10.",
    "Intuicja często polega na znalezieniu reprezentacji, w której struktura staje się widoczna.": "Intuition often means finding a representation in which the structure becomes visible.",
    "Opcjonalny moduł. Zapytaj, czy model „widzi” symetrię tak jak człowiek, czy odtwarza i składa poznane strategie.": "Optional module. Ask whether the model “sees” symmetry as a human does, or reproduces and combines learned strategies.",
    "Co znaczy nieskończony zapis?": "What does an infinite decimal mean?",
    "W liczbach rzeczywistych: 0,999… = 1": "In the real numbers: 0.999… = 1",
    "0,999… := lim": "0.999… := lim",
    "Droga przez granicę": "The limit route",
    "Skończone przybliżenia to 1 − 10": "The finite approximations are 1 − 10",
    "Gdy n rośnie, 10": "As n grows, 10",
    "Granica wynosi 1.": "The limit is 1.",
    "Jawnie powiedz: w liczbach rzeczywistych i przy zwykłej definicji rozwinięcia dziesiętnego.": "State explicitly that this is in the real numbers, using the usual definition of a decimal expansion.",
    "Zagadka · nie pokazuj alarmu": "Puzzle · do not reveal the warning",
    "„Dowód”, że 1 = 2. Wskaż pierwszy niedozwolony krok.": "A “proof” that 1 = 2. Identify the first invalid step.",
    "Najpierw decyzja": "Choose first",
    "Które przejście jest pierwszym błędem?": "Which transition contains the first error?",
    "Nie oceniaj tylko absurdalnego wyniku.": "Do not judge only by the absurd conclusion.",
    "Zatrzymaj slajd po pokazaniu wszystkich kroków. Poproś o numer przejścia i warunek, który może być potrzebny. Nie zdradzaj jeszcze odpowiedzi.": "Pause after revealing all the steps. Ask for the number of the transition and the condition it may require. Do not reveal the answer yet.",
    "Pierwszy błąd, nie tylko zły wynik": "Find the first error, not merely the wrong result",
    "Warunek ukryty w zwykłym „skracaniu”": "A condition hidden inside ordinary “cancellation”",
    "dzielimy przez a − b": "divide by a − b",
    "Dzielenie przez zero nie jest dozwolone.": "Division by zero is not allowed.",
    "POLECENIE DLA AGENTA": "INSTRUCTION FOR THE AGENT",
    "„Sprawdź każdy krok. Wskaż pierwszy błąd i nazwij złamany warunek.”": "“Check every step. Identify the first error and name the violated condition.”",
    "Czyta:": "Reads:",
    "Wylicza:": "Computes:",
    "Odrzuca:": "Rejects:",
    "dzielenie przez 0": "division by zero",
    "Dobry audyt sprawdza": "A good audit checks",
    "lokalne przejścia i ich warunki": "local transitions and their conditions",
    ", a nie tylko końcowe zdanie.": ", not just the final statement.",
    "Założenie b≠0 jest potrzebne dopiero przy ostatnim dzieleniu przez b. Pierwszy błąd następuje wcześniej.": "The assumption b≠0 is needed only for the final division by b. The first error occurs earlier.",
    "MATEMATYKA": "MATHEMATICS",
    "Elegancki niedozwolony krok": "An elegant but invalid step",
    "Każda linia wygląda znajomo, ale jeden warunek niszczy cały dowód.": "Every line looks familiar, but one violated condition destroys the entire proof.",
    "FAKTY": "FACTS",
    "„Przekonujący cytat”": "A “convincing quotation”",
    "Model może wymyślić źródło, datę lub cytat, który brzmi idealnie i nie istnieje.": "A model may invent a source, date, or quotation that sounds perfect but does not exist.",
    "zostało sprawdzone": "has been verified",
    "W matematyce proś o kontrprzykład, mały przypadek, drugi sposób lub formalną kontrolę. W faktach sprawdzaj źródło poza modelem.": "In mathematics, ask for a counterexample, a small case, another method, or a formal check. For factual claims, verify the source outside the model.",
    "Konkretny problem": "A concrete problem",
    "Ile prostokątów ma plansza m×k pól?": "How many rectangles are in an m×k grid of cells?",
    "Definicja problemu": "Problem definition",
    "Liczymy prostokąty o bokach na liniach siatki. Kwadraty też są prostokątami.": "We count rectangles whose sides lie on grid lines. Squares count as rectangles.",
    "m+1 linii": "m+1 lines",
    "k+1 linii": "k+1 lines",
    "Pierwszy strzał": "First guess",
    "To liczba pól, nie wszystkich prostokątów.": "That is the number of cells, not all rectangles.",
    "Wybierz granice": "Choose the boundaries",
    "Dwie linie pionowe wyznaczają lewy i prawy bok.": "Two vertical lines determine the left and right sides.",
    "Drugi kierunek": "The other direction",
    "Dwie linie poziome wyznaczają górę i dół.": "Two horizontal lines determine the top and bottom.",
    "Wzór ogólny": "General formula",
    "Zacznij od 2×3, nie od 8×8. Poproś o wskazanie czterech linii ograniczających jeden prostokąt.": "Start with 2×3, not 8×8. Ask the audience to point out the four lines that bound one rectangle.",
    "Agent tworzy testowalny artefakt": "The agent creates a testable artifact",
    "Program znajduje błąd „o jeden”. Matematyka wyjaśnia wzór.": "The program finds an off-by-one error. Mathematics explains the formula.",
    "„Napisz program dla m×k. Najpierw przetestuj 1×1, 1×2 i 2×3.”": "“Write a program for an m×k grid. Test 1×1, 1×2, and 2×3 first.”",
    "Wybór dwóch pionowych i dwóch poziomych linii.": "Choose two vertical and two horizontal lines.",
    "Uruchom zweryfikowaną symulację": "Run the verified simulation",
    "$ gotowy do uruchomienia testów": "$ ready to run tests",
    "Komputer sprawdził:": "The computer checked:",
    "konkretne przypadki.": "specific instances.",
    "Matematyka wyjaśniła:": "Mathematics explained:",
    "każdy prostokąt odpowiada wyborowi czterech linii.": "each rectangle corresponds to a choice of four lines.",
    "To zaprogramowana ilustracja wcześniej zweryfikowanego przebiegu, nie nagranie prawdziwej sesji. Dla 8×8 wynik to 1296; kwadratów jest 204, niekwadratowych prostokątów 1092.": "This is a programmed illustration of a previously verified run, not a recording of a real session. For 8×8 the total is 1296: 204 squares and 1092 non-square rectangles.",
    "Wiele sukcesów nie daje dowodu": "Many successes do not constitute a proof",
    "Kiedy n²+n+41 przestaje być pierwsza?": "When does n²+n+41 stop being prime?",
    "Dla n=0,1,…,39 otrzymujemy liczby pierwsze.": "For n=0,1,…,39, the values are prime.",
    "Uruchom rzeczywiste obliczenie": "Run the actual computation",
    "$ szukam pierwszej porażki…": "$ searching for the first failure…",
    "czekam": "waiting",
    "Komputer znalazł:": "The computer found:",
    "pierwszy kontrprzykład w badanej kolejności.": "the first counterexample in the tested sequence.",
    "Matematyka nadal potrzebuje:": "Mathematics still needs:",
    "powodu, dlaczego pojawia się właśnie tam.": "an explanation of why it appears exactly there.",
    "Obliczenie jest wykonywane w przeglądarce. Przypomnij, że 1 nie jest ani pierwsza, ani złożona.": "The computation runs in the browser. Remind the audience that 1 is neither prime nor composite.",
    "Kontrprzykład nie jest przypadkiem": "The counterexample is not an accident",
    "Podstaw n = p−1": "Substitute n = p−1",
    "Przypadek brzegowy": "Edge case",
    "Wynik 1 nie jest ani pierwszy, ani złożony.": "The value 1 is neither prime nor composite.",
    "To dobry przykład różnicy między znalezieniem wyniku i wyjaśnieniem mechanizmu.": "This is a good example of the difference between finding a result and explaining the mechanism.",
    "Ten sam problem · inna rola AI": "The same problem · a different role for AI",
    "Jedno pytanie diagnostyczne. Jedna wskazówka. Stop.": "One diagnostic question. One hint. Stop.",
    "Myślę, że dla 8×8 odpowiedź to 64. Oto moja próba.": "I think the answer for 8×8 is 64. Here is my attempt.",
    "Ile pionowych linii ogranicza osiem kolumn pól?": "How many vertical lines bound eight columns of cells?",
    "Dziewięć. Wybieram lewą i prawą granicę.": "Nine. I choose the left and right boundaries.",
    "Ile nieuporządkowanych par można wybrać z dziewięciu linii?": "How many unordered pairs can be chosen from nine lines?",
    "C(9,2)=36. W obu kierunkach: 36·36=1296.": "C(9,2)=36. In both directions: 36·36=1296.",
    "Teraz samodzielnie przenieś metodę na planszę 2×3.": "Now apply the method to a 2×3 grid on your own.",
    "WARUNEK SUKCESU": "SUCCESS CRITERION",
    "Uczeń rozwiązuje nowy wariant i wyjaśnia metodę bez transkryptu AI.": "The student solves a new variant and explains the method without the AI transcript.",
    "ujawnia rzeczywisty punkt startu.": "reveals the genuine starting point.",
    "Diagnoza:": "Diagnosis:",
    "jedno pytanie znajduje lukę.": "one question locates the gap.",
    "nie zastępuje kolejnego kroku ucznia.": "does not replace the student's next step.",
    "mały przypadek testuje metodę.": "a small case tests the method.",
    "Transfer:": "Transfer:",
    "nowy problem potwierdza naukę.": "a new problem demonstrates learning.",
    "To jeden z głównych slajdów wykładu. Odegraj rozmowę z uczniem i naprawdę czekaj na odpowiedź.": "This is one of the talk's central slides. Act out the conversation with a student and genuinely wait for an answer.",
    "Prompt, który wspiera naukę": "A prompt that supports learning",
    "Zły skrót kontra dobra umowa o współpracy": "A bad shortcut versus a good working agreement",
    "SŁABO": "WEAK",
    "„Rozwiąż to.”": "“Solve this.”",
    "Nie określa celu, roli ani momentu zatrzymania.": "It defines neither the goal, the role, nor when to stop.",
    "LEPIEJ": "BETTER",
    "„Uczę się tego tematu. Nie rozwiązuj całego zadania. Najpierw zadaj jedno pytanie diagnostyczne. Potem daj jedną wskazówkę i poczekaj. Na końcu poproś mnie o wyjaśnienie własnymi słowami. Oto moja próba: …”": "“I am learning this topic. Do not solve the whole problem. First ask one diagnostic question. Then give one hint and wait. At the end, ask me to explain the method in my own words. Here is my attempt: …”",
    "Nie chodzi o magiczną formułę. Prompt tworzy procedurę, która wymusza udział ucznia.": "This is not a magic formula. The prompt establishes a procedure that requires the student to participate.",
    "Pięć pytań kontrolnych": "Five checking questions",
    "Zanim zaufasz odpowiedzi": "Before you trust an answer",
    "Jakie założenie jest tu użyte?": "What assumption is being used?",
    "Jaki jest najmniejszy przykład?": "What is the smallest example?",
    "Jaki jest przypadek brzegowy?": "What is the edge case?",
    "Czy mogę sprawdzić to inną metodą, narzędziem lub źródłem?": "Can I check this with another method, tool, or source?",
    "Czy umiem wyjaśnić wynik bez rozmowy z AI?": "Can I explain the result without the AI conversation?",
    "„Drugi dowód” z tego samego modelu może powtórzyć ten sam błąd. Niezależność metody ma znaczenie.": "A “second proof” from the same model may repeat the same error. Independence of method matters.",
    "Nie tylko Codex": "Not only Codex",
    "Co działa w każdym dozwolonym narzędziu AI?": "What works with any permitted AI tool?",
    "Proś o": "Ask for",
    "pytania": "questions",
    ", nie tylko odpowiedzi.": ", not only answers.",
    "Proś o jawne": "Ask for explicit",
    "założenia": "assumptions",
    "przypadki brzegowe": "edge cases",
    "Oddziel": "Separate",
    "rachunek od dowodu": "calculation from proof",
    "Zapytaj:": "Ask:",
    "co zmieniłoby tę odpowiedź?": "what would change this answer?",
    "Sprawdź samodzielnie, z nauczycielem, podręcznikiem albo kodem.": "Verify it yourself, with a teacher, a textbook, or code.",
    "Produkt jest wymienny. Nawyki kontroli i uczenia się są trwałe.": "Tools come and go. Habits of verification and learning endure.",
    "„Najpierw spróbuj” w praktyce": "Putting “try first” into practice",
    "Daj sobie 3–5 minut przed otwarciem AI": "Give yourself 3–5 minutes before using AI",
    "Co wiem?": "What do I know?",
    "Definicje, dane, podobne zadania.": "Definitions, given information, similar problems.",
    "Czego próbuję?": "What am I trying?",
    "Rysunek, hipoteza, rachunek, mały przykład.": "A diagram, hypothesis, calculation, or small example.",
    "Gdzie jest blokada?": "Where am I stuck?",
    "Przekaż AI konkretny punkt utknięcia, nie całe zadanie.": "Give AI the specific sticking point, not the entire task.",
    "Minuta patrzenia w pustą kartkę nie jest jeszcze próbą. Chodzi o zapisany ślad rozumowania.": "A minute spent staring at a blank page is not yet an attempt. Produce a written trace of your reasoning.",
    "Używaj tak, żeby nie stracić nauki": "Use it without losing the learning",
    "AI w szkole: sześć zasad": "AI at school: six rules",
    "Stosuj zasady zadania.": "Follow the rules of the assignment.",
    "Jeśli nauczyciel mówi „bez AI”, nie używaj AI.": "If the teacher says “no AI,” do not use AI.",
    "Zacznij od własnej próby.": "Begin with your own attempt.",
    "Zachowaj szkic, pytania i miejsce utknięcia.": "Keep your draft, questions, and the point where you got stuck.",
    "Proś najpierw o pytanie lub wskazówkę.": "Ask for a question or hint first.",
    "Nie oddawaj celu nauki maszynie.": "Do not hand the learning objective to the machine.",
    "Chroń dane i cudze materiały.": "Protect data and other people's material.",
    "Bez nazwisk, ocen, zdrowia, haseł, prywatnych rozmów i nieuprawnionych kopii.": "Do not share names, grades, health information, passwords, private conversations, or unauthorized copies.",
    "Ujawnij pomoc, gdy trzeba.": "Disclose assistance when required.",
    "Napisz, czy AI pomogło w pomyśle, kodzie, stylu lub sprawdzeniu.": "State whether AI helped with the idea, code, style, or verification.",
    "Odpowiedzialność zostaje u ciebie.": "Responsibility remains yours.",
    "Na egzaminie, konkursie i w pracy ocenianej obowiązują osobne reguły.": "Exams, competitions, and assessed work have their own rules.",
    "To nie jest moralizowanie o oszustwie, tylko praktyczne zarządzanie ryzykiem i celem nauki.": "This is not moralizing about cheating. It is practical management of risk and learning goals.",
    "Warunki są częścią twierdzenia": "Conditions are part of the theorem",
    "Małe twierdzenie Fermata i test pierwszości": "Fermat's little theorem and a primality test",
    "TWIERDZENIE": "THEOREM",
    "p pierwsza ⇒ a": "p prime ⇒ a",
    "Dla każdego całkowitego a.": "For every integer a.",
    "WERSJA DLA NWD=1": "VERSION FOR gcd=1",
    "Ta postać prowadzi do testu Fermata.": "This form leads to the Fermat test.",
    "PSEUDOPIERWSZA": "PSEUDOPRIME",
    "n złożona, gcd(a,n)=1": "n composite, gcd(a,n)=1",
    "Mimo to a": "yet a",
    "Używaj p wyłącznie dla liczby pierwszej, n dla badanego kandydata, a dla podstawy.": "Use p only for a prime, n for the candidate being tested, and a for the base.",
    "Sprawdzanie nie jest dowodem": "Passing a check is not a proof",
    "341 przechodzi test Fermata dla podstawy 2": "341 passes the base-2 Fermat test",
    "Nie potwierdzaj hipotezy. Szukaj złożonego n, które przejdzie test.": "Do not confirm the hypothesis. Find a composite n that passes the test.",
    "Sprawdzę gcd(2,n)=1 i warunek 2": "I will check gcd(2,n)=1 and the condition 2",
    "$ czekam na test": "$ waiting to run the test",
    "FAKTORYZACJA": "FACTORIZATION",
    "Liczba jest złożona.": "The number is composite.",
    "Przejście testu nie dowodzi pierwszości.": "Passing the test does not prove primality.",
    "WYJAŚNIENIE": "EXPLANATION",
    "≡1 (mod 31), więc warunek zachodzi modulo obu czynników.": "≡1 (mod 31), so the condition holds modulo both factors.",
    "Obliczenie w terminalu jest rzeczywiste. Wyjaśnienie wykorzystuje czynniki 11 i 31, a nie gigantyczną potęgę.": "The terminal performs a real computation. The explanation uses the factors 11 and 31 rather than an enormous power.",
    "Sprawdź po wykładzie": "Explore after the talk",
    "Slajdy, źródła i laboratoria": "Slides, sources, and labs",
    "Stabilna zasada:": "Stable principle:",
    "weryfikuj twierdzenia i warunki.": "verify claims and conditions.",
    "Zmienna część:": "Moving target:",
    "funkcje produktów, modele i benchmarki szybko się starzeją.": "product features, models, and benchmarks age quickly.",
    "Daj uczniom chwilę na zeskanowanie kodu. Zaznacz, że strona zawiera źródła i ćwiczenia bez wysyłania danych.": "Give students a moment to scan the code. Point out that the site includes sources and exercises that do not send their data anywhere.",
    "Nie oddawaj": "Do not hand over",
    "odpowiedzialności.": "responsibility.",
    "Zlecaj obliczenia, szkice i testy. Zachowaj": "Delegate calculations, drafts, and tests. Keep",
    "rozumienie, kontrolę i wybór kierunku.": "understanding, control, and the choice of direction.",
    "Po użyciu AI: czy rozumiem więcej i umiem to wyjaśnić?": "After using AI: do I understand more, and can I explain it?",
    "Konkretne zadanie na wieczór: użyj AI raz jako korepetytora, nie wykonawcy, i zapisz, co zmieniło się w twoim rozumowaniu.": "A concrete task for tonight: use AI once as a tutor rather than a task-doer, and write down what changed in your understanding.",
    "Dodatek · bibliografia": "Appendix · bibliography",
    "Transformer i mechanizm uwagi": "The transformer and attention mechanism",
    "Uczenie wykonywania instrukcji": "Training models to follow instructions",
    "Weryfikacja krok po kroku": "Step-by-step verification",
    "Rozumowanie i uczenie ze wzmocnieniem": "Reasoning and reinforcement learning",
    "Źródła projektu": "Project sources",
    "Pełna bibliografia, zastrzeżenia i data sprawdzenia": "Full bibliography, caveats, and verification date",
    "Slajd zapasowy do pytań. Część produktowa jest najbardziej podatna na dezaktualizację.": "Backup slide for questions. Product-specific material is the most likely to become outdated.",
    "Trzy rozróżnienia, których warto pilnować": "Three distinctions worth preserving",
    "Wynik a rozumienie": "Result versus understanding",
    "Poprawna odpowiedź nie rozstrzyga, czy model ma ludzką intuicję lub doświadczenie świata.": "A correct answer does not establish whether a model has human intuition or experience of the world.",
    "Kandydat a idea naukowa": "Candidate versus scientific idea",
    "Nowa kombinacja może być użyteczna, ale nowość, znaczenie i autorstwo wymagają niezależnej oceny.": "A new combination may be useful, but novelty, significance, and authorship require independent evaluation.",
    "Sprawdzenie a zaufanie": "Verification versus trust",
    "Ufamy w granicach, w których znamy metodę kontroli i akceptujemy koszt błędu.": "Trust is justified only where we know how to check the result and accept the cost of error.",
    "Materiał zapasowy. Nie używaj automatycznie w podstawowych 35 minutach.": "Backup material. Do not include it automatically in the core 35-minute talk.",
    "Ścieżka": "Track",
    "Rdzeń 35 min": "Core 35 min",
    "Rdzeń + matematyka": "Core + mathematics",
    "Pełna": "Full",
    "Plan ścieżki:": "Track time:",
    "Ta prezentacja wymaga JavaScriptu do nawigacji. Treść i źródła pozostają dostępne w pliku HTML.": "This presentation requires JavaScript for navigation. Its content and sources remain available in the HTML file.",
})

TEXT.update({
    "Jak używać AI w zadaniach wymagających myślenia, nie oddając mu kontroli nad rozumowaniem.": "How to use AI for thinking-intensive tasks without giving up control of the reasoning.",
    "Do czego najczęściej używasz AI?": "What do you most often use AI for?",
    "AI może wykonać za nas część czynności": "AI can perform some tasks for us",
    "i dostarczyć": "and provide a",
    "gotowy wynik.": "ready-made result.",
    "Jaki token najlepiej pasuje jako następny?": "Which token fits best as the next one?",
    "Najpierw tokenizer dzieli tekst na": "First, the tokenizer splits the text into",
    "Dla każdej pozycji model oblicza, jak silnie połączyć ją z poszczególnymi wcześniejszymi pozycjami.": "At each position, the model computes how strongly to connect it with each earlier position.",
    "Wagi określają wkład wcześniejszych pozycji": "The weights determine how much earlier positions contribute",
    "Maska przyczynowa nadaje przyszłym pozycjom wagę zero": "The causal mask gives future positions zero weight",
    "Każda warstwa łączy informacje z kontekstu i przekształca wektory reprezentujące tokeny.": "Each layer combines contextual information and transforms the vectors representing the tokens.",
    "uwaga + sieć feed-forward": "attention + feed-forward network",
    "Trening wstępny": "Pretraining",
    "Pretrening: L(θ) = −Σ log p": "Pretraining: L(θ) = −Σ log p",
    "Dostrajanie po treningu": "Post-training",
    "Posttrening nadal zmienia parametry.": "Post-training still changes the parameters.",
    "Model może wykonać więcej kroków, prób i sprawdzeń wyniku podczas odpowiedzi.": "While answering, the model may perform more steps, attempts, and checks.",
    "System pozwala modelowi czytać pliki, uruchamiać kod i analizować wyniki narzędzi.": "The system lets the model read files, run code, and analyse tool outputs.",
    "To pętla działania wokół gotowego modelu.": "This is an action loop around a trained model.",
    "Więcej czasu obliczeń pozwala sprawdzić kilka sposobów rozwiązania i poprawić błędy.": "More computation time allows several solution paths to be checked and errors to be corrected.",
    "Python, CAS, testy i programy sprawdzające dowody tworzą zewnętrzny brudnopis.": "Python, computer algebra systems, tests, and proof checkers provide an external scratchpad.",
    "AI może proponować hipotezy i rozwiązania. Trudniej jej ocenić ich wartość.": "AI can propose hypotheses and possible solutions. Assessing their value is harder.",
    "Nie potrafi niezawodnie ocenić, czy propozycja jest naprawdę nowa, ważna i poprawna.": "It cannot reliably judge whether a proposal is genuinely new, important, and correct.",
    "Intuicja często polega na takim zapisaniu problemu, aby jego struktura stała się widoczna.": "Intuition often means rewriting a problem so that its structure becomes visible.",
    "Skrót algebraiczny po zdefiniowaniu granicy": "Algebraic shortcut after defining the limit",
    "każdy krok osobno i warunki jego wykonania": "each step separately and the conditions required for it",
    "Brzmi pewnie ≠ jest prawdziwe": "Sounds confident ≠ is true",
    "Elegancko zapisany błąd": "An elegantly written error",
    "Plansza ma m wierszy i k kolumn. Liczymy prostokąty o bokach na liniach siatki; kwadraty też się liczą.": "The board has m rows and k columns. We count rectangles whose sides lie on grid lines; squares count too.",
    "k+1 linii pionowych": "k+1 vertical lines",
    "m+1 linii poziomych": "m+1 horizontal lines",
    "Dwie linie poziome wyznaczają górny i dolny bok.": "Two horizontal lines determine the top and bottom sides.",
    "Agent tworzy program, który można sprawdzić": "The agent creates a program that can be run and checked",
    "Wybór dwóch z m+1 linii poziomych i dwóch z k+1 linii pionowych.": "Choose two of the m+1 horizontal lines and two of the k+1 vertical lines.",
    "Uruchom test": "Run the test",
    "Dla jakiego pierwszego n wartość n²+n+41 nie jest pierwsza?": "For which first n is n²+n+41 not prime?",
    'for (let n = 0; ; n++) { const value = n*n + n + 41; if (classify(value) !== "prime") { console.log({n, value}); break; } }': '''for (let n = 0; ; n++) {
  const value = n*n + n + 41;
  if (classify(value) !== "prime") {
    console.log({n, value});
    break;
  }
}''',
    "Podstaw n = c−1": "Substitute n = c−1",
    "c=41": "c=41",
    "(n) = n²+n+c": "(n) = n²+n+c",
    "(c−1) = (c−1)²+(c−1)+c": "(c−1) = (c−1)²+(c−1)+c",
    "= c²": "= c²",
    "Polecenie, które wyręcza, kontra polecenie, które pomaga się uczyć": "A prompt that does the work versus one that supports learning",
    "Jaki jest najprostszy mały przykład, na którym mogę to sprawdzić?": "What is the simplest small example I can use to check this?",
    "Te same nawyki pomagają przy różnych narzędziach AI": "The same habits help with different AI tools",
    "Na którym dokładnie kroku utknąłem?": "At exactly which step am I stuck?",
    "Pokaż AI własną próbę i wskaż konkretny punkt, w którym potrzebujesz pomocy.": "Show AI your own attempt and identify the exact point where you need help.",
    "Nie pozwól, aby narzędzie wykonało za ciebie właśnie tę część, której masz się nauczyć.": "Do not let the tool perform the very part you are meant to learn.",
    "Nie wpisuj nazwisk, ocen, informacji o zdrowiu, haseł ani prywatnych rozmów. Nie przesyłaj materiałów, których nie wolno ci udostępniać.": "Do not enter names, grades, health information, passwords, or private conversations. Do not upload material you are not allowed to share.",
    "p pierwsza i NWD(a,p)=1 ⇒ a": "p prime and gcd(a,p)=1 ⇒ a",
    "n złożona, NWD(a,n)=1": "n composite, gcd(a,n)=1",
    "NWD(2,n)=1": "gcd(2,n)=1",
    "Sprawdzę NWD(2,n)=1 i warunek 2": "I will check gcd(2,n)=1 and the condition 2",
    "Jeśli mimo to a": "If nevertheless a",
    "≡ 1 (mod n), liczba n jest pseudopierwsza przy podstawie a.": "≡ 1 (mod n), then n is a pseudoprime to base a.",
    "10 | 340 i 2": "10 | 340 and 2",
    "≡1 (mod 11); 5 | 340 i 2": "≡1 (mod 11); 5 | 340 and 2",
    "≡1 (mod 31). Ponieważ NWD(11,31)=1, otrzymujemy 2": "≡1 (mod 31). Since gcd(11,31)=1, we obtain 2",
    "≡1 (mod 341).": "≡1 (mod 341).",
})


ATTR = {
    "35-minutowy popularnonaukowy wykład o AI, matematyce i myśleniu dla klas 7-8 i liceum.": "A 35-minute popular-science talk about AI, mathematics, and thinking for middle- and high-school students.",
    "Uczeń i zbudowany z kart pomocnik AI wspólnie oglądają geometryczną zagadkę": "A student and a card-built AI assistant examine a geometric puzzle",
    "Rząd geometrycznych postaci połączonych łukami o różnej grubości": "A row of geometric figures connected by arcs of different thickness",
    "Uczniowie z pomocnikiem AI badają nasiona pomysłów, z których wyrasta geometryczne drzewo": "Students and an AI assistant examine idea seeds growing into a geometric tree",
    "Przykładowy podział wyrazu matematyka na tokeny": "Illustrative tokenization of the word mathematics",
    "Schemat wielu warstw transformera": "Diagram of multiple transformer layers",
    "Trzy kroki analizy Codex": "Three steps in a Codex audit",
    "Szachownica osiem na osiem z zaznaczonym prostokątem": "An eight-by-eight chessboard with a highlighted rectangle",
    "Przykładowa rozmowa ucznia z Codexem": "Example conversation between a student and Codex",
    "Pięć zasad zilustrowanych w eksperymencie": "Five rules illustrated in the experiment",
    "Rozmowa ucznia z Codexem": "Conversation between a student and Codex",
    "Sterowanie prezentacją": "Presentation controls",
    "Poprzedni slajd": "Previous slide",
    "Następny slajd": "Next slide",
    "Notatki prowadzącego": "Speaker notes",
    "Zamknij notatki": "Close notes",
    "Wróć do strony głównej": "Return to the home page",
    "Wybór języka": "Language selection",
    "Tytuł": "Title",
    "Sonda": "Poll",
    "Teza": "Claim",
    "Gra w następny token": "Next-token game",
    "Tokeny": "Tokens",
    "Atencja": "Attention",
    "Atencja matematycznie": "Attention formula",
    "Trening": "Training",
    "Dlaczego matematyka": "Why mathematics",
    "Fałszywy dowód": "False proof",
    "Pewność": "Confidence",
    "Codex szuka pomysłu": "Codex searches for an idea",
    "Codex uruchamia test": "Codex runs a test",
    "Euler i narzędzia": "Euler and tools",
    "Uczeń pracuje z Codexem": "Student works with Codex",
    "Dobry prompt": "Good prompt",
    "Zasady": "Rules",
    "Zabawa z Fermatem": "Playing with Fermat",
    "Finał": "Finale",
    "Źródła": "Sources",
    "Ściąga prowadzącego": "Speaker cheat sheet",
}

ATTR.update({
    "Interaktywny wykład o AI, matematyce i odpowiedzialnym myśleniu dla klas 7-8 i liceum.": "An interactive talk about AI, mathematics, and responsible thinking for middle- and high-school students.",
    "Rząd geometrycznych figur połączonych łukami o różnej grubości": "A row of geometric figures connected by arcs of different thickness",
    "Następny token": "Next token",
    "Tokenizacja": "Tokenization",
    "MODUŁ TECHNICZNY · można pominąć": "TECHNICAL MODULE · may be skipped",
    "Ilustracyjny podział słowa matematyka na tokeny": "Illustrative tokenization of the word mathematics",
    "Mechanizm uwagi": "Attention mechanism",
    "Wzór uwagi": "Attention formula",
    "MODUŁ TECHNICZNY · macierze": "TECHNICAL MODULE · matrices",
    "Attention Q K V równa się softmax z Q K transponowane plus maska M podzielone przez pierwiastek z d k, razy V": "Attention Q K V equals softmax of Q K transpose plus mask M, divided by the square root of d k, multiplied by V",
    "Maska i wagi": "Mask and weights",
    "MODUŁ TECHNICZNY · przypadek 4 tokenów": "TECHNICAL MODULE · a four-token example",
    "Trójkątna macierz uwagi: każdy token może ważyć tylko siebie i wcześniejsze tokeny": "Triangular attention matrix: each token may weight only itself and earlier tokens",
    "MODUŁ TECHNICZNY · architektura": "TECHNICAL MODULE · architecture",
    "Schemat stosu warstw transformera": "Diagram of a stack of transformer layers",
    "Trening i użycie": "Training and use",
    "Pętla agenta": "Agent loop",
    "Pomysły i intuicja": "Ideas and intuition",
    "MODUŁ MATEMATYCZNY · intuicja": "MATHEMATICAL MODULE · intuition",
    "MODUŁ MATEMATYCZNY · granica": "MATHEMATICAL MODULE · limits",
    "zero przecinek dziewięć okres definiujemy jako granicę jeden minus dziesięć do potęgi minus n": "zero point nine recurring is defined as the limit of one minus ten to the power minus n",
    "Audyt dowodu": "Proof audit",
    "Płynność i prawda": "Fluency and truth",
    "Prostokąty m×k": "Rectangles in an m×k grid",
    "Plansza osiem na osiem z zaznaczonym prostokątem": "An eight-by-eight grid with a highlighted rectangle",
    "Program i dowód": "Program and proof",
    "Euler: eksperyment": "Euler: experiment",
    "MODUŁ MATEMATYCZNY · eksperyment": "MATHEMATICAL MODULE · experiment",
    "Euler: wyjaśnienie": "Euler: explanation",
    "MODUŁ MATEMATYCZNY · wyjaśnienie": "MATHEMATICAL MODULE · explanation",
    "Dla f p od n równego n kwadrat plus n plus p, wartość w p minus jeden wynosi p kwadrat": "For f sub p of n equal to n squared plus n plus p, the value at p minus one is p squared",
    "Dla f c od n równego n kwadrat plus n plus c, wartość w c minus jeden wynosi c kwadrat": "For f sub c of n equal to n squared plus n plus c, the value at c minus one is c squared",
    "AI jako korepetytor": "AI as a tutor",
    "Rozmowa ucznia z agentem AI": "A conversation between a student and an AI agent",
    "Prompt korepetytorski": "Tutor prompt",
    "Zanim zaufasz": "Before you trust",
    "Każde narzędzie AI": "Any AI tool",
    "Własna próba": "Your own attempt",
    "AI w szkole": "AI at school",
    "Twierdzenie Fermata": "Fermat's theorem",
    "MODUŁ MATEMATYCZNY · teoria liczb": "MATHEMATICAL MODULE · number theory",
    "Jeśli p jest pierwsza, to a do p jest przystające do a modulo p": "If p is prime, then a to the power p is congruent to a modulo p",
    "a do p minus jeden jest przystające do jeden modulo p": "a to the power p minus one is congruent to one modulo p",
    "Jeśli p jest pierwsza i a jest względnie pierwsza z p, to a do p minus jeden jest przystające do jeden modulo p": "If p is prime and a is coprime to p, then a to the power p minus one is congruent to one modulo p",
    "Pseudopierwsza 341": "The pseudoprime 341",
    "MODUŁ MATEMATYCZNY · kontrprzykład": "MATHEMATICAL MODULE · counterexample",
    "Materiały": "Resources",
    "Kod QR prowadzący do publicznej strony prezentacji": "QR code linking to the public presentation website",
    "Pełne źródła": "Full sources",
    "Wybierz ścieżkę prezentacji": "Choose a presentation track",
})

NORMALIZED_TEXT = {" ".join(key.split()): value for key, value in TEXT.items()}

ALLOWED_UNCHANGED_TEXT = {
    "Bartosz Naskręcki",
    "UAM/CCAI",
    "Ab",
    "A(Q,K,V) = softmax((QK",
    "T",
    "+ M) / √d",
    "k",
    ")V",
    "Q",
    "K",
    "V",
    "Q = XW",
    "K = XW",
    "V = XW",
    "L(θ) = −Σ log p",
    "(x",
    "t",
    "|x",
    "t)",
    "Agent",
    "n→∞",
    "−n",
    "9x = 9",
    "x = 1",
    "a = b ≠ 0",
    "a² = ab",
    "a² − b² = ab − b²",
    "(a − b)(a + b) = b(a − b)",
    "a + b = b",
    "ALARM",
    "a − b = 0",
    "a=b",
    "a−b=0",
    "m·k?",
    "C(m+1,2)",
    "C(k+1,2)",
    "R(m,k)",
    "C(m+1,2)·C(k+1,2)",
    "Plan",
    "C(m+1,2) · C(k+1,2)",
    "- range(width)",
    "+ range(width + 1)",
    "codex · rectangle_demo.py",
    "n²+n+41",
    'for (let n = 0; ; n++) { const value = n*n + n + 41; if (classify(value) !== "prime") return {n, value}; }',
    'for (let n = 0; ; n++) { const value = n*n + n + 41; if (classify(value) !== "prime") { console.log({n, value}); break; } }',
    "f",
    "p",
    "c",
    "(n) = n²+n+p",
    "(p−1) = (p−1)²+(p−1)+p",
    "= p²",
    "p=41",
    "n=40",
    "c=1, n=0",
    "AI",
    "≡ a (mod p)",
    "gcd(a,p)=1 ⇒ a",
    "p−1",
    "≡ 1 (mod p)",
    "n−1",
    "≡ 1 (mod n).",
    "agent · fermat_test.py",
    "gcd(2,n)=1",
    "≡1 (mod n).",
    "JavaScript · modular exponentiation",
    "TEST",
    "≡ 1 (mod 341)",
    "≡1 (mod 11), 2",
    "nasqret.github.io/czy-ai-zastapi-nasza-glowe",
    "OpenAI (2024)",
    "OpenAI Codex",
    "PL",
    "EN",
    "Copyright © 2026 Bartosz Naskręcki. All rights reserved.",
    "N",
    "O",
    "F",
}

LOCALIZED_ATTRIBUTES = {
    "alt",
    "aria-label",
    "content",
    "data-title",
    "data-track-label",
    "lang",
    "title",
}

ALLOWED_UNCHANGED_ATTRIBUTES = {
    "width=device-width, initial-scale=1",
    "dark",
    "Transformer",
    "Gauss",
    "0,999...",
}


class Translator(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.output: list[str] = []
        self.missing_text: set[str] = set()
        self.missing_attributes: set[tuple[str, str]] = set()

    def translate_attribute(self, key: str, value: str) -> str:
        if key == "lang" and value == "pl":
            return "en"
        translated = ATTR.get(value)
        if translated is not None:
            return translated
        if key in LOCALIZED_ATTRIBUTES and value not in ALLOWED_UNCHANGED_ATTRIBUTES:
            self.missing_attributes.add((key, value))
        return value

    def render_attributes(self, attrs: list[tuple[str, str | None]]) -> str:
        rendered = []
        for key, value in attrs:
            if value is None:
                rendered.append(key)
                continue
            translated = self.translate_attribute(key, value)
            rendered.append(f'{key}="{escape(translated, quote=True)}"')
        return f" {' '.join(rendered)}" if rendered else ""

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.output.append(f"<{tag}{self.render_attributes(attrs)}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.output.append(f"<{tag}{self.render_attributes(attrs)}/>")

    def handle_endtag(self, tag: str) -> None:
        self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            self.output.append(data)
            return
        normalized = " ".join(stripped.split())
        has_explicit_translation = (
            stripped in TEXT or normalized in NORMALIZED_TEXT
        )
        translated = TEXT.get(stripped)
        if translated is None:
            translated = NORMALIZED_TEXT.get(normalized, stripped)
        if (
            translated == stripped
            and not has_explicit_translation
            and normalized not in ALLOWED_UNCHANGED_TEXT
            and re.search(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]", normalized)
        ):
            self.missing_text.add(normalized)
        prefix = data[: len(data) - len(data.lstrip())]
        suffix = data[len(data.rstrip()):]
        self.output.append(f"{prefix}{translated}{suffix}")

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.signature: list[tuple[str, str, tuple[tuple[str, str | None], ...]]] = []
        self.slides: list[tuple[str, str, str]] = []
        self.note_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        invariant_attrs = tuple(
            (key, "<localized>" if key in LOCALIZED_ATTRIBUTES else value)
            for key, value in attrs
        )
        self.signature.append(("start", tag, invariant_attrs))
        values = dict(attrs)
        classes = (values.get("class") or "").split()
        if tag == "section" and "slide" in classes:
            self.slides.append((
                values.get("id", ""),
                values.get("data-track", ""),
                values.get("data-duration", ""),
            ))
        if tag == "aside" and "notes" in classes:
            self.note_count += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.signature.append(("end", tag, ()))

    def handle_endtag(self, tag: str) -> None:
        self.signature.append(("end", tag, ()))


class LanguageAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.content: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = " ".join(data.split())
        if stripped:
            self.content.append(stripped)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in LOCALIZED_ATTRIBUTES and value:
                self.content.append(value)


def parse_structure(html: str) -> StructureParser:
    parser = StructureParser()
    parser.feed(html)
    return parser


def assert_same_structure(source: str, result: str) -> StructureParser:
    source_parser = parse_structure(source)
    result_parser = parse_structure(result)
    if source_parser.signature != result_parser.signature:
        raise RuntimeError("English output does not preserve the Polish HTML structure")
    if source_parser.slides != result_parser.slides:
        raise RuntimeError("Slide IDs, tracks, or durations differ between PL and EN")
    if source_parser.note_count != result_parser.note_count:
        raise RuntimeError("Speaker-note counts differ between PL and EN")
    return result_parser


def polish_lexicon() -> set[str]:
    source_words: set[str] = set()
    english_words: set[str] = set()
    for source, translation in [*TEXT.items(), *ATTR.items()]:
        source_words.update(re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}", source.lower()))
        english_words.update(re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}", translation.lower()))
    return source_words - english_words - {"naskręcki"}


def assert_no_polish(result: str) -> None:
    parser = LanguageAuditParser()
    parser.feed(result)
    audited_items = [
        item for item in parser.content if item not in ALLOWED_UNCHANGED_TEXT
    ]
    content = "\n".join(audited_items)
    without_name = content.replace("Naskręcki", "")
    diacritics = sorted(set(re.findall(r"[ĄĆĘŁŃÓŚŹŻąćęłńóśźż]", without_name)))
    tokens = {
        token.lower()
        for token in re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}", without_name)
    }
    suspicious_words = sorted(tokens & polish_lexicon())
    translated_source_phrases = {
        " ".join(source.split())
        for source, translation in [*TEXT.items(), *ATTR.items()]
        if source != translation
    }
    unchanged_phrases = sorted(
        {
            " ".join(item.split())
            for item in audited_items
            if " ".join(item.split()) in translated_source_phrases
        }
    )
    if diacritics or suspicious_words or unchanged_phrases:
        details = []
        if diacritics:
            details.append(f"Polish diacritics: {', '.join(diacritics)}")
        if suspicious_words:
            details.append(f"Polish words: {', '.join(suspicious_words)}")
        if unchanged_phrases:
            details.append(
                "Unchanged Polish phrases: " + ", ".join(unchanged_phrases)
            )
        raise RuntimeError("Polish-language residue in EN output; " + "; ".join(details))


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    parser = Translator()
    parser.feed(source)
    if parser.missing_text or parser.missing_attributes:
        details = []
        if parser.missing_text:
            details.append(
                "untranslated text:\n  - " + "\n  - ".join(sorted(parser.missing_text))
            )
        if parser.missing_attributes:
            details.append(
                "untranslated attributes:\n  - "
                + "\n  - ".join(
                    f"{key}={value!r}"
                    for key, value in sorted(parser.missing_attributes)
                )
            )
        raise RuntimeError("\n".join(details))
    result = "".join(parser.output)
    structure = assert_same_structure(source, result)
    assert_no_polish(result)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(result, encoding="utf-8")
    print(
        f"Built {TARGET.relative_to(ROOT)}: "
        f"{len(structure.slides)} slides, {structure.note_count} speaker notes, "
        "structure preserved, Polish residue audit passed"
    )


if __name__ == "__main__":
    main()
