# სუდოკუს ამომხსნელი როგორც შეზღუდვის დაკმაყოფილების პრობლემა

სუდოკუ არის ლოგიკაზე დაფუძნებული თამაში. თავიდან არის მოცემული 9x9
დაფა, 9 კვადრატული 3x3 რეგიონით, რომელთა ნაწილი არის შევსებული 1-9
რიცხვებით. მოთამაშის მიზანია შეავსოს ყველა ცარიელი უჯრა ისე, რომ
არცერთი სვეტი, სტრიქონი და რეგიონი არ შეიცავდეს ერთსა და იმავე რიცხვს
ერთზე მეტჯერ.

CSP (Constraint Satisfaction Problem) არის მათემატიკური პრობლემა, რომლის
მდგომარეობაც უნდა აკმაყოფილებდეს რაღაც შეზღუდვებს. ის შედგება სამი
კომპონენტისგან. ცვლადები, დომეინი ანუ ყველა შესაძლო მნიშვნელობა, რაც
ცვლადებმა შეიძლება მიიღონ და შეზღუდვები.

სუდოკუში ცვლადები არიან ცარიელი უჯრები, დომეინი არის
1-9
რიცხვები
და
შეზღუდვები არის, რომ
არცერთ
სვეტში,
სტრიქონში
ან
რეგიონში
არ
უნდა
იყოს თითო რიცხვი
ერთზე
მეტჯერ
და
ყველა
უჯრა
შევსებული უნდა იყოს.

## გამოყენება

თითოეული Sudoku წარმოდგენილია თითო სტრიქონში 81 ციფრით და წერტილით. უჯრები დანომრილია ზედა მარცხენა უჯრიდან ქვედა მარჯვენა უჯრამდე.

მაგალითად:</br> .94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8

ერთი ფაილი შეიძლება შეიცავდეს რამდენიმე Sudoku-ს(რამდენიმე სტრიქონს)

პროგრამა ეშვება ტერმინალიდან:

```python csp-solver.py input.file output.file```

## იმპლემენტაცია

ძებნისთვის გამოვიყენე სტანდარტული რეკურსიული ალგორითმი
ბექთრექინგით, რომელიც ლექციაზე გავიარეთ და გავარჩიეთ. ამ ძებნას
სტანდარტული ძებნის სახე აქვს ერთი განსხვავებით : იმახსოვრებს წინა
სთეითს და თუ რეკურსიულმა გამოძახებამ არასწორი პასუხი დააბრუნა წინა
სთეითს აღადგენს.

```pseudo
function BACKTRACKING-SEARCH(csp) returns solution/failure
	return RECURSIVE-BACKTRACKING({}, csp)

function RECURSIVE-BACKTRACKING(assignment, csp) return solution/failure
	if assignment is complete then return assignment
	var ← SELECT-UNASSIGNED-VARIABLE(VARIABLES[csp], assignment, csp)
	for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
		if value is consistent with assignment given CONSTRAINTS[csp] then
			add {var = value} to assignment
			result ← RECURSIVE-BACKTRACKING(assignment, csp)
			if result ≠ failure then return result
			remove {var = value} from assignment
	return failure
```

იმისთვის, რომ პროგრამამ უფრო სწრაფად იმუშავოს დავუმატე ფორვარდ
ჩექინგი. ანუ წინასწარ ამოწმებს არჩეული მნიშვნელობის ცვლადისთვის
მინიჭება შეცდომას ხო არ გამოიწვევს. ამის დამსახურებით არ მოხდება ისეთი
შემთხვევა, როცა ჯერ ყველა 1- ებით ივსება, მერე ბოლოდან იწბებს 2- ად
გადაკეთებას. არ მოუწევს ისეთი უაზრობების ჩაყოლა, რომლებიც თავიდანვე
არღვევენ შეზღუდვებს. ჩემს იმპლემენტაციაში ყოველ ჯერზე შემოწმების
ნაცვლად თავიდან გადავუყვები ერთხელ და ვნახულობ რომელ ცვლადს რა
მნიშვნელობები შეიძლება მიენიჭოს შეზღუდვების დარღვევის გარეშე და
ვინახავ ლექსიკონში. ამის შემდეგ ყოველ ჯერზე როცა რომელიმე ცვლადს
რამე მნიშვნელობას ვანიჭებ მის ყველა მეზობელს ვუშლი ამ მნიშვნელობას
და ნებისმიერ დროს გარანტირებული მაქვს, რომ ამ ლექსიკონში არსებული
ნებისმიერი მნიშვნელობის თავის ცვლადზე მინიჭება არ დაარღვევს
შეზღუდვას.

იმის გამო, რომ სუდოკუ პატარა და მარტივი პრობლემაა გადავწყვიტე
კლასების გარეშე დამეწერა. მთელი ჩემი ალგორითმი არის ერთი
რეკურსიული ძებნა ფორვარდჩექინგით და ერთი ევრისტიკით. წერის დროს
ვცადე არაერთი მოდიფიკაცია, მაგრამ მათგან მხოლოდ ერთმა გაამართლა და
მხოლოდ ის დავტოვე.

MRV (Minimum Remaining Value) ირჩევს იმ ცვლადს, რომელსაც ყველაზე ცოტა
შესაძლო მნიშვნელობა აქვს ისე, რომ შეზღუდვები არ ირღვეოდეს. ეგ გზა ორი
მიზეზით არის კარგი. პირველი და მთავარი არის ის, რომ რაც უფრო ცოტა
ვარიანტია უფრო დიდია იმის ალბათობა, რომ სწორი მნიშვნელობა
ავირჩიოთ. ასევე მცირდება ბრენჩინგ ფაქტორი.

MD (Max Degree) ირჩევს ცვლადს, რომელისაც ყველაზე მაღალი ხარისხი აქვს
იმ შემთხვევაში თუ თანაბარი რაოდენობის ელემენტებით შეიძლება შეივსოს
ცვლადები. ხარისხი არის იგივე მეზობლების რაოდენობა ანუ იმცვლადების
რაოდენობა, რომელებიც არჩეული ცვლადით არიან შეზღუდულები და ჯერ არ
არიან შევსებულები. ამ მიდგომამ არ იმუშავა, რადგან მხოლოდ MRV
საკმარისად კარგ შედეგს გვაძლევს და ეს გზა ზედმეტ გამოთვლით ძალას
მოითხოვს ამ პრობლემისთვის.

LCV ირჩევს იმ მნიშვნელობას, რომელიც ყველაზე ცოტას ზღუდავს. ანუ
ცვლადს ვანიჭებთ იმ მნიშვნელობას, რომელიც ყველაზე ცოტა მის მეზობელს
აქვს. ამ მიდგომამაც არ გაამართლა, რადგან იმაზე მეტ რესურსს მოითხოვს,
ვიდრე სარგებელი მოაქვს. სისწრაფისთვის ყოველ ჯერზე ძებნის ნაცვლად
შენახული მქონდა ყველა სვეტის, სტრიქონის და რეგიონის ინფორმაცია და
მათი შეცვლის დროს ვააფდეითებდი, რამაც პროგრამა ააჩქარა, მაგრამ არა
საგრძნობლად.

Arc Consistency ამოწმებს რომელიმე მნიშვნელობის ჩასმა რომელიმე ორს
შორის შეზღუდვის დარღვევის გარეშე რომელიმე მეზობელს შესაძლო
მნიშვნელობების რაოდენობას ხო არ უნულებს. თუ ეს ასე ხდება ანუ ამ
მნიშვნელობის ჩასმა აქ არ შეგვიძლია, რადგან მეზობელს თუ არ დაუთმობს
მაგ მნიშვნელობას ისე ის პირობა არ სრულდება ყველა ცვლადს რომ რამე
მნიშვნელობა უნდა ჰქონდეს მინიჭებული. ამის შედეგ ყველაზე უცნაური იყო.
ლექციებიდან როგორი წარმოდგენაც მქონდა, დარწმუნებული ვიყავი, რომ
პროგრამა აჩქარდებოდა, მაგრამ აჩქარების ნაცვლად ძალიან ცოტათი
შეანელა.

## შედეგები
კომპიუტერი:</br>
```HP Notebook – 14-an013nr```</br>
```CPU: AMD Quad-Core E2-7110 (1.8 GHz, 2 MB cache)```</br>
```RAM: 8GB DDR3L-1600```</br>
```Drive: Kingston SSD SA400S37```

ყველა სუდოკუზე ხუთი გაშვების საშუალო:</br>
MRV – 6.91</br>
MRV+MD – 11.13</br>
MRV+LCV(slow) – 14.48</br>
MRV+LCV(fast) – 12.33</br>
MRV+AC – 7.64

დასკვნა:</br>
სუდოკუ არის პატარა და მარტივი CSP, რის გამოც ის სტანდარტული
მოდიფიკაციები რაც დიდ პროექტებზე ძალიან კარგად მუშაობს, აქ უფრო მეტ
ცუდს აკეთებს, ვიდრე კარგს. 1000 პრობლემის 7- ზე ნაკლებ წამში ამოხსნა
უკვე ისეთი შედეგია, რაზე კარგიც არავის არ დასჭირდება სუდოკუსთვის.
