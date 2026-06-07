"""Build the static English presentation from the Polish canonical HTML."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path


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

NORMALIZED_TEXT = {" ".join(key.split()): value for key, value in TEXT.items()}


class Translator(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.output: list[str] = []

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        rendered = []
        for key, value in attrs:
            if value is None:
                rendered.append(key)
                continue
            translated = "en" if key == "lang" and value == "pl" else ATTR.get(value, value)
            rendered.append(f'{key}="{escape(translated, quote=True)}"')
        suffix = f" {' '.join(rendered)}" if rendered else ""
        self.output.append(f"<{tag}{suffix}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        rendered = []
        for key, value in attrs:
            if value is None:
                rendered.append(key)
                continue
            translated = "en" if key == "lang" and value == "pl" else ATTR.get(value, value)
            rendered.append(f'{key}="{escape(translated, quote=True)}"')
        suffix = f" {' '.join(rendered)}" if rendered else ""
        self.output.append(f"<{tag}{suffix}>")

    def handle_endtag(self, tag: str) -> None:
        self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            self.output.append(data)
            return
        translated = TEXT.get(stripped)
        if translated is None:
            translated = NORMALIZED_TEXT.get(" ".join(stripped.split()), stripped)
        prefix = data[: len(data) - len(data.lstrip())]
        suffix = data[len(data.rstrip()):]
        self.output.append(f"{prefix}{translated}{suffix}")

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")


def main() -> None:
    parser = Translator()
    parser.feed(SOURCE.read_text(encoding="utf-8"))
    result = "".join(parser.output)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(result, encoding="utf-8")
    print(f"Built {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
