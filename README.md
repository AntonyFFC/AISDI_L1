# AISDI_L1 - Wyszukiwanie Mediany w Wielu Tablicach

## Zadanie: Opis problemu
Dane jest `m` tablic o rozmiarach `n0`, `n1`, .., `nm-1`, zawierające dane liczbowe. Dla każdej tablicy znana jest wartość maksymalna i minimalna.
Znaleźć medianę zbioru liczb, które są zapisane w powyżej opisany sposób.
Mediana zbioru liczb to wartość środkowa w przypadku gdy wielkość zbioru jest liczbą nieparzystą. W przypadku parzystej liczby elementów mediana to średnia arytmetyczna dwóch wartości środkowych.

**Założenia podane w zadaniu:**
* `m > 0`
* `n0 + n1 + .. + nm-1 > 0`

**Wytyczne:**
* Zaprojektować algorytmy i struktury danych, które zapewnią najmniejszą możliwie złożoność obliczeniową i najmniejszą złożoność pamięciową.
* Opisać wszelkie przyjęte założenia, które nie znajdują się w opisie zadania, a mają wpływ na algorytmy lub implementację.
* Wszelkie algorytmy powinny być zaimplementowane w programie, nie należy korzystać z funkcji bibliotecznych (np. do sortowania).
* Zaprojektować i zaimplementować testy automatyczne. 

---

## Przyjęte Założenia (Niewymienione w zadaniu)
Aby zrealizować projekt, przyjęto następujące założenia doprecyzowujące specyfikację:
1. **Brak początkowego sortowania:** Zakładam, że podane tablice wejściowe **nie są posortowane**. Wymusza to algorytm, który nie polega na indeksowaniu w posortowanej strukturze.
2. **Typ danych:** Liczby w tablicach są liczbami całkowitymi (`int`). 
3. **Zwracany typ mediany:** W przypadku parzystej liczby wszystkich elementów, obliczona mediana może być ułamkiem (średnia arytmetyczna dwóch liczb całkowitych), dlatego funkcja zwraca typ zmiennoprzecinkowy (`float`).
4. **Duplikaty:** Algorytm jest odporny na powtarzające się wartości (duplikaty) w obrębie jednej oraz wielu tablic.

---

## Opis Algorytmu
Zastosowano podejście oparte na **wyszukiwaniu binarnym po wyniku (Binary Search on Answer)**. 

Zamiast łączyć wszystkie tablice i je sortować (co drastycznie zwiększyłoby złożoność pamięciową), algorytm wykorzystuje fakt, że znamy absolutne minimum (globalne minimum) oraz absolutne maksimum (globalne maksimum) ze wszystkich tablic. 

1. Wyznaczany jest przedział poszukiwań od globalnego minimum do globalnego maksimum.
2. W każdej iteracji algorytm "zgaduje" środkową wartość (mid) i zlicza wszystkie elementy we wszystkich tablicach, które są od niej mniejsze lub równe.
3. W zależności od zliczonej liczby elementów, przedział poszukiwań jest zwężany (w lewo lub w prawo).
4. **Dla nieparzystej liczby elementów:** Zwracana jest znaleziona wartość.
5. **Dla parzystej liczby elementów:** Algorytm po znalezieniu pierwszej wartości środkowej, wykonuje dodatkowe, pojedyncze przejście po tablicach w celu znalezienia najmniejszej liczby ostro większej od pierwszej wartości środkowej (z odpowiednim zabezpieczeniem przed duplikatami). Następnie wyciągana jest z nich średnia.

---

## Analiza Złożoności

* **Złożoność pamięciowa:** $O(1)$
  Algorytm nie tworzy żadnych nowych tablic, nie kopiuje danych i nie używa rekurencji. Do działania potrzebuje jedynie kilku zmiennych pomocniczych do zliczania elementów i trzymania wskaźników przedziału, niezależnie od rozmiaru danych wejściowych. Jest to optymalna i najmniejsza możliwa złożoność pamięciowa.

* **Złożoność obliczeniowa:** $O(N \log R)$
  Gdzie $N$ to całkowita liczba elementów we wszystkich tablicach ($n_0 + n_1 + \dots + n_{m-1}$), a $R$ to rozstęp (zakres) między globalnym maksimum a globalnym minimum. Pętla wyszukiwania binarnego wykonuje się $\log R$ razy, a wewnątrz niej następuje liniowe przejście po wszystkich $N$ elementach. W przypadku parzystej liczby elementów dodawane jest jeszcze jedno przejście liniowe $O(N)$, co nie zmienia ogólnej asymptotycznej klasy złożoności algorytmu.

---

## Wady i Zalety Rozwiązania

### Zalety:
* **Ekstremalnie niska złożoność pamięciowa:** Brak konieczności konkatenacji i realokacji pamięci sprawia, że algorytm poradzi sobie z gigantycznymi zbiorami danych, o ile tylko zmieszczą się one oryginalnie w pamięci RAM.
* **Brak konieczności sortowania:** Spełnia ścisłe wytyczne zadania, unikając kosztownego pamięciowo sortowania.
* **Pełna kontrola nad logiką:** Dzięki zastosowaniu wyszukiwania binarnego kod sprawnie omija problem z łączeniem wielu struktur o różnych rozmiarach.

### Wady:
* **Zależność od rozstępu danych (Range):** Jeśli różnica między globalnym minimum a globalnym maksimum jest gigantyczna (np. skrajne wartości dla 64-bitowych intów), liczba iteracji pętli binarnej nieznacznie rośnie.
* **Narzut w języku Python:** Ze względu na to, że Python jest językiem interpretowanym, wielokrotne iterowanie po listach za pomocą podwójnych pętli `for` zajmuje więcej czasu rzeczywistego (wall-clock time) niż wykonanie wbudowanej funkcji `.sort()` (która pod spodem działa w zoptymalizowanym języku C jako Timsort). Jednakże algorytm wygrywa na poziomie teoretycznej złożoności i optymalizacji zasobów komputera.

---

## Eksperyment Wydajnościowy (Python vs C)
Aby udowodnić, że czas wykonania w środowisku testowym wynika w dużej mierze z narzutu interpretera języka Python, przeprowadzono dodatkowy eksperyment. Ten sam algorytm został zaimplementowany w języku C i skompilowany z użyciem flagi optymalizacji `-O3` (kompilator GCC). 

**Wyniki testu dla 20 tablic (łącznie ok. 600 000 elementów):**
* **Czas wykonania w Pythonie:** ~0.3643 s
* **Czas wykonania w C:** ~0.0019 s

**Wniosek:** Skompilowany kod w C okazał się blisko **300 razy szybszy**. Potwierdza to, że sam zaprojektowany algorytm jest optymalny, a wydłużony czas działania programu głównego jest naturalną cechą języków interpretowanych oraz dynamicznie typowanych, a nie błędem logiki czy złym zarządzaniem pamięcią.