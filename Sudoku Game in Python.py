#zapoctovy program sudoku
import pygame as pg
import random
import numpy as np

# Nazev hry
pg.display.set_caption("SUDOKU HRA PRO VOLNÉ CHVÍLE")

pg.init()
font = pg.font.SysFont("none", 55)
font2 = pg.font.SysFont("none", 20)
font3 = pg.font.SysFont("none", 77)
screen = pg.display.set_mode((575, 730))

grid0 =[
		[7, 8, 0, 4, 0, 0, 1, 2, 0],
		[6, 0, 0, 0, 7, 5, 0, 0, 9],
		[0, 0, 0, 6, 0, 1, 0, 7, 8],
		[0, 0, 7, 0, 4, 0, 2, 6, 0],
		[0, 0, 1, 0, 5, 0, 9, 3, 0],
		[9, 0, 4, 0, 6, 0, 0, 0, 5],
		[0, 7, 0, 3, 0, 0, 0, 1, 2],
		[1, 2, 0, 0, 0, 7, 4, 0, 0],
		[0, 4, 9, 2, 0, 6, 0, 0, 7]
	]


#sudoku zadání
grid_default = np.zeros((9,9), dtype=int)
grid_reseni = np.zeros((9,9), dtype=int)
#pozice kurzoru
x_pos = 0
y_pos = 0
#velikost sloupce/řádku v pixelech
dif = 540/9
#proměnná pro input z klavesnice
input_value_from_keyboard = 0
#hlida jestli se uzivatel posouva po plose kurzorem mysi nebo sipkama
ukazatel_pozice_na_obrazovce = 0


#varianta - klasické = 0, killer, windoku
varianta_sudoku = 0
kontrola = 1


#funkce na kopírování
def copy_grid(original_grid, destination_grid):
    for i in range(0,9):
        for j in range(0,9):
            destination_grid[i][j] = original_grid[i][j]
#pro získání pozice myši
def get_cord(pos):
    global x_pos
    x_pos = (pos[0] - 15)//dif
    global y_pos
    y_pos = (pos[1] - 15)//dif
    global x_pos_
#vykreslí mřížku, čáry    
def draw_background(varianta, kontrola):
    if varianta == "killer":
        #vykresli dve sede diagonalni cary typicke pro killer sudoku
        pg.draw.line(screen, pg.Color("gray"), pg.Vector2(20, 550),pg.Vector2(550, 20), 3)
        pg.draw.line(screen, pg.Color("gray"), pg.Vector2(20, 20),pg.Vector2(550, 550), 3)
        #vykresli krizek do ctverecku instrukci
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(200, 710),pg.Vector2(230, 680), 3)
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(200, 680),pg.Vector2(230, 710), 3)
    if varianta == "windoku":
        #vykresli krizek do ctverecku instrukci
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(380, 710),pg.Vector2(410, 680), 3)
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(380, 680),pg.Vector2(410, 710), 3)
        #vykresli barevne ctverce pro windoku
        for i in range(1,8):
            for j in range(1,8):
                if i != 4 and j != 4:
                    pg.draw.rect(screen, (200, 30, 130), (i * dif + 15, j * dif + 15, dif + 1, dif + 1))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 540, 540), 7)
    i = 1   
    while (i * 60) < 540:
        tloustka = 4
        if i % 3 > 0:
            tloustka = 2
        else:
            tloustka = 7
        #screen = kam se to má vykreslit, barva, prvni Vector2 x-ove a y-ove souradnice začátku čáry, druhy Vector2 je konec, pak tloustka
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * dif) + 15, 15), pg.Vector2((i * dif) + 15, 555), tloustka)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * dif) + 15), pg.Vector2(555, (i * dif) + 15), tloustka)
        i += 1

    #vykresli ctverecky do instrukci
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(20,680,30,30), 5)
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(200,680,30,30), 5)
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(380,680,30,30), 5)
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(380,630,30,30), 5)
    #krizek ukazuje jake sudoku zrovna hrajeme   
    if varianta == 0:
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(20, 710),pg.Vector2(50, 680), 3)
        pg.draw.line(screen, pg.Color("blue"), pg.Vector2(20, 680),pg.Vector2(50, 710), 3)
    if kontrola % 2 == 0:
        #vykresli krizek do ctverecku instrukci kontroly spravnosti
        pg.draw.line(screen, pg.Color("red"), pg.Vector2(380, 660),pg.Vector2(410, 630), 3)
        pg.draw.line(screen, pg.Color("red"), pg.Vector2(380, 630),pg.Vector2(410, 660), 3)

#označí vybraný čtvereček
def draw_box():
    global x_pos, y_pos
    for i in range(2):
        if x_pos < 0:
            x_pos = 8
        if x_pos > 8:
            x_pos = 0
        if y_pos < 0:
            y_pos = 8
        if y_pos > 8:
            y_pos = 0
        pg.draw.line(screen, (0, 0, 255), (x_pos * dif + 12, (y_pos + i)*dif + 15), (x_pos * dif + dif + 18, (y_pos + i)*dif + 15), 7)
        pg.draw.line(screen, (0, 0, 255), ((x_pos + i)* dif + 15, y_pos * dif + 15 ), ((x_pos + i) * dif + 15, y_pos * dif + dif + 15), 7)


#Vypise vsechna cisla do mrizky
def cisla(grid):
    global grid_default
    radek = 0
    offset_radek = 29
    offset_sloupec = 36
    while radek < 9:
        sloupec = 0
        while sloupec < 9:
            output = grid[radek][sloupec]
            if str(output) == "0":        
                n_text = font.render(str(" "), True, pg.Color("white"))
            elif grid_default[radek][sloupec] == grid[radek][sloupec]:
                n_text = font.render(str(output), True, (100,100,100))            
            else:
                n_text = font.render(str(output), True, pg.Color("black"))
                #vybarvi jiz vyplnena policka
                #pg.draw.rect(screen, (0, 166, 233), (sloupec * dif + 15, radek * dif + 15, dif + 1, dif + 1))
            screen.blit(n_text, pg.Vector2((sloupec * dif) + offset_sloupec, (radek * dif) + offset_radek))
            sloupec += 1
        radek += 1
        

    
#zkontroluje, zda je dane cislo 'n' muze byt na pozici x,y  
#varianta: 0 = klasicke sudoku, 1 = killer/diagonalni sudoku, 2 = windoku      
def valid_number(grid, x, y, n, varianta):
    #kontrola radku
    for i in range(0,9):
        if grid[i][y] == n:
            return False
    #kontrola sloupce
    for j in range(0,9):
        if grid[x][j] == n:
            return False
    #kontrola ctverce
    k = x//3
    l = y//3
    for i in range(k * 3, k * 3 + 3):
        for j in range(l * 3, l * 3 + 3):
            if grid[i][j] == n:
                return False        
    #killer sudoku/ diagonalni sudoku
    if varianta == "killer":
        if x == y:    
            for i in range(0,9):
                if grid[i][i] == n:
                    return False
        if x + y == 8:
            for i in range(0,9):
                for j in range(0,9):
                    if i + j == 8 and grid[i][j] == n:
                        return False
    #windoku má ještě 4 čtverce navíc uvnitř klasického sudoku, kde se čísla 1-9 nemohou opakovat
    if varianta == "windoku":
        if (1 <= x and x <= 3) and (1 <= y and y <= 3):
            for i in range(1,4):
                for j in range(1,4):
                    if grid[i][j] == n:
                        return False              
        if (1 <= x and x <= 3) and (5 <= y and y <= 7):
            for i in range(1,4):
                for j in range(5,8):
                    if grid[i][j] == n:
                        return False
        if (5 <= x and x <= 7) and (5 <= y and y <= 7):
            for i in range(5,8):
                for j in range(5,8):
                    if grid[i][j] == n:
                        return False
    return True


#generuje sudoku - vybere náhodně řádek a sloupec a přiřadí tam náhodné číslo
#kontroluje jestli jsou nová čísla vložena podle pravidel, takto přiřadí 17 čísel, pak sudoku vyřeší a doplní dalších 22 náhodných čísel z řešení
def sudoku_generator(grid, varianta):
    loop = True
    counter = 0
    grid_temp = np.zeros((9,9), dtype=int)
    while loop:
        row = random.randrange(0,9)
        col = random.randrange(0,9)
        value = random.randrange(1,10)
        if grid[row][col] == 0 and valid_number(grid, row, col, value, varianta):
            grid[row][col] = value
            counter += 1
        if counter == 17:
            loop = False  
    counter = 0
    copy_grid(grid, grid_temp)
    sudoku_solver(grid_temp, 0, varianta)
    while counter < 22:
        row = random.randrange(0,9)
        col = random.randrange(0,9)
        if grid[row][col] == 0:
            grid[row][col] = grid_temp[row][col]
            counter += 1

#vyresi cele sudoku        
def sudoku_solver(grid, grafika, varianta):
    pg.event.pump()
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j] == 0:
                for k in range(1,10):
                    if valid_number(grid, i, j, k, varianta):
                        grid[i][j] = k
                        if grafika:
                            global kontrola
                            global x_pos, y_pos
                            x_pos = j
                            y_pos = i
                            draw_background(varianta, kontrola)
                            cisla(grid)
                            draw_box()
                            instruction(varianta_sudoku)
                            pg.display.update()
                            pg.time.delay(80)
                        if sudoku_solver(grid, grafika,varianta):
                            return True
                        grid[i][j] = 0
                        if grafika:
                            screen.fill((255, 255, 255))
                            draw_background(varianta, kontrola)
                            cisla(grid)
                            instruction(varianta_sudoku)
                            pg.display.update()
                            pg.time.delay(100)   
                return False
    return True

def sudoku_solver_one_position(grid, x, y, varianta):
    grid_temp = np.zeros((9,9), dtype=int)
    copy_grid(grid, grid_temp)
    sudoku_solver(grid_temp, 0, varianta)
    value = grid_temp[x][y]
    return int(value)

def print_sudoku_to_console(grid):
    pole = [0, 0, 0, 0, 0, 0, 0, 0, 0] 
    for i in range(0,9):
        for j in range(0,9):
            pole[j] = grid[i][j] 
        print(pole)
        pole = [0, 0, 0, 0, 0, 0, 0, 0, 0] 
    print(" ")
    
def kontrola_vysledku(grid, grid_solution, varianta):
    counter = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == grid_solution[i][j]: 
                counter +=1
    if counter == 81:
        return True
    else:
        return False
    
def prubezna_kontrola(grid, grid_solution):
    offset_radek = 29
    offset_sloupec = 36
    for i in range(0,9):
        for j in range(0,9):
            output = grid[i][j]
            if grid[i][j] != 0 and grid_solution[i][j] != grid[i][j]:
                n_text = font.render(str(output), True, pg.Color("red"))
                screen.blit(n_text, pg.Vector2((j * dif) + offset_sloupec, (i * dif) + offset_radek))

def instruction(varianta):
    text1 = font2.render(" D - NÁVRAT K VÝCHOZÍMU SUDOKU", 1, (0, 0, 0))
    text11 = font2.render(" R - VYGENEROVÁNÍ NOVÉHO SUDOKU", 1, (0, 0, 0))
    text12 = font2.render(" H - NÁPOVĚDA V POLÍČKU", 1, (0, 0, 0))
    text13 = font2.render(" ENTER - CELÉ ŘEŠENÍ S VIZUALIZACÍ", 1, (0, 0, 0))
    text14 = font2.render(" S - CELÉ ŘEŠENÍ", 1, (0, 0, 0))
    text15 = font2.render(" DELETE/BACKSPACE - VYMAZÁNÍ ČÍSLA", 1, (0, 0, 0))
    text16 = font2.render(" ESCAPE - UKONČIT HRU", 1, (0, 0, 0))
    text17 = font2.render(" KONTROLA ", 1, (250, 0, 0))
    text3 = font3.render("GRATULUJI  :)", 1, (244, 0, 0))
    text4 = font3.render("KE    SPRÁVNÉMU", 1, (244, 0, 0))
    text5 = font3.render("ŘEŠENÍ !!!!", 1, (244, 0, 0))
    text6 = font2.render("KLASICKÉ SUDOKU", 1, (0, 250, 0))
    text7 = font2.render("KILLER SUDOKU", 1, (0, 250, 0))
    text8 = font2.render("WINDOKU", 1, (0, 250, 0))
    text_navod_klasicke_sudoku1 = font2.render("KLASICKÉ SUDOKU: VYPLŇTE POLÍČKA", 1, (0, 0, 0))
    text_navod_klasicke_sudoku2 = font2.render("ČÍSLY 1 - 9 TAK, ABY SE NEOPAKOVALA", 1, (0, 0, 0))
    text_navod_klasicke_sudoku3 = font2.render("VE SLOUPCI, ŘÁDKU A ČTVERCI", 1, (0, 0, 0))
    text_navod_killer1 = font2.render("KILLER SUDOKU: ČÍSLA 1 - 9 SE NESMÍ ", 1, (0, 0, 0))
    text_navod_killer2 = font2.render("OPAKOVAT V ŘÁDKU, SLOUPCI, ČTVERCI ", 1, (0, 0, 0))
    text_navod_killer3 = font2.render("A NA ŠEDÝCH DIAGONÁLÁCH ", 1, (0, 0, 0))
    text_navod_windoku1 = font2.render("WINDOKU: ČÍSLA 1 - 9 SE NESMÍ ", 1, (0, 0, 0))
    text_navod_windoku2 = font2.render("OPAKOVAT V ŘÁDKU, SLOUPCI, ČTVERCI ", 1, (0, 0, 0))
    text_navod_windoku3 = font2.render("A V BAREVNÝCH ČTVERCÍCH ", 1, (0, 0, 0))
    screen.blit(text1, (20, 565))	
    screen.blit(text11, (20, 580))
    screen.blit(text12, (20, 595))
    screen.blit(text14, (20, 610))
    screen.blit(text13, (20, 625))
    screen.blit(text15, (20, 640))
    screen.blit(text16, (20, 655))
    screen.blit(text17, (420, 637))
    if varianta == 0:
        screen.blit(text_navod_klasicke_sudoku1, (300, 560))
        screen.blit(text_navod_klasicke_sudoku2, (300, 580))
        screen.blit(text_navod_klasicke_sudoku3, (300, 600))
    elif varianta == "killer":
        screen.blit(text_navod_killer1, (300, 560))
        screen.blit(text_navod_killer2, (300, 580))
        screen.blit(text_navod_killer3, (300, 600))
    else:
        screen.blit(text_navod_windoku1, (300, 560))
        screen.blit(text_navod_windoku2, (300, 580))
        screen.blit(text_navod_windoku3, (300, 600))
    screen.blit(text6, (59, 687))
    screen.blit(text7, (239, 687))
    screen.blit(text8, (420, 687))
    if kontrola_vysledku(grid0, grid_reseni, varianta):
        screen.blit(text3, (25, 170))
        screen.blit(text4, (25, 250))
        screen.blit(text5, (25, 330))

    
    

pocitadlo_cyklu_programu = 0
copy_grid(grid0, grid_default)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
		# Get the mouse position to insert number
        if event.type == pg.MOUSEBUTTONDOWN: 
            ukazatel_pozice_na_obrazovce = 1
            pos = pg.mouse.get_pos()
            get_cord(pos)  
		# Get the number to be inserted if key pressed
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x_pos -= 1
                ukazatel_pozice_na_obrazovce = 1
            if event.key == pg.K_RIGHT:
                x_pos += 1
                ukazatel_pozice_na_obrazovce = 1
            if event.key == pg.K_UP:
                y_pos -= 1
                ukazatel_pozice_na_obrazovce = 1
            if event.key == pg.K_DOWN:
                y_pos += 1
                ukazatel_pozice_na_obrazovce = 1
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_1:
                input_value_from_keyboard = 1
            if event.key == pg.K_2:
                input_value_from_keyboard = 2
            if event.key == pg.K_3:
                input_value_from_keyboard = 3
            if event.key == pg.K_4:
                input_value_from_keyboard = 4
            if event.key == pg.K_5:
                input_value_from_keyboard = 5
            if event.key == pg.K_6:
                input_value_from_keyboard = 6
            if event.key == pg.K_7:
                input_value_from_keyboard = 7
            if event.key == pg.K_8:
                input_value_from_keyboard = 8
            if event.key == pg.K_9:
                input_value_from_keyboard = 9
            if event.key == pg.K_RETURN:
                sudoku_solver(grid0, 1, varianta_sudoku)
            # If R pressed regenerate new sudoku
            if event.key == pg.K_r:
                grid0 = np.zeros((9,9), dtype=int)
                sudoku_generator(grid0,varianta_sudoku)
                copy_grid(grid0, grid_default)    
                pocitadlo_cyklu_programu = 0
			# If D is pressed reset the board to default
            if event.key == pg.K_d:
                grid0 = np.zeros((9,9), dtype=int)
                copy_grid(grid_default, grid0)                                
            if event.key == pg.K_s:
                copy_grid(grid_reseni, grid0)
                print_sudoku_to_console(grid0)
            if event.key == pg.K_DELETE:
                if grid_default[int(y_pos)][int(x_pos)] == 0:
                    grid0[int(y_pos)][int(x_pos)] = 0
            if event.key == pg.K_BACKSPACE:
                if grid_default[int(y_pos)][int(x_pos)] == 0:
                    grid0[int(y_pos)][int(x_pos)] = 0
            if event.key == pg.K_h:
                if grid_default[int(y_pos)][int(x_pos)] == 0:
                    grid0[int(y_pos)][int(x_pos)] = grid_reseni[int(y_pos)][int(x_pos)]
                    
                
    if input_value_from_keyboard != 0:
        if grid_default[int(y_pos)][int(x_pos)] == 0:
            grid0[int(y_pos)][int(x_pos)]= input_value_from_keyboard
        input_value_from_keyboard = 0
        
    
    
    
    screen.fill(pg.Color("white"))
    draw_background(varianta_sudoku, kontrola)
    cisla(grid0)  
    
    #po vygenerovani noveho sudoku se vytvori nove reseni
    if pocitadlo_cyklu_programu == 0:
        copy_grid(grid_default, grid_reseni)
        sudoku_solver(grid_reseni, 0, varianta_sudoku)
    
         
    
    
    #prubezna kontrola
    if y_pos == 10 and (x_pos == 6 or x_pos == 7 or x_pos == 8):
        kontrola += 1
    if kontrola % 2 == 0:
        prubezna_kontrola(grid0, grid_reseni)
        
 
    pocitadlo_cyklu_programu += 1
    
    instruction(varianta_sudoku)
    
    if y_pos == 11 and (x_pos == 0 or x_pos == 1 or x_pos == 2):
        varianta_sudoku = 0
        grid0 =[
        		[7, 8, 0, 4, 0, 0, 1, 2, 0],
        		[6, 0, 0, 0, 7, 5, 0, 0, 9],
        		[0, 0, 0, 6, 0, 1, 0, 7, 8],
        		[0, 0, 7, 0, 4, 0, 2, 6, 0],
        		[0, 0, 1, 0, 5, 0, 9, 3, 0],
        		[9, 0, 4, 0, 6, 0, 0, 0, 5],
        		[0, 7, 0, 3, 0, 0, 0, 1, 2],
        		[1, 2, 0, 0, 0, 7, 4, 0, 0],
        		[0, 4, 9, 2, 0, 6, 0, 0, 7]
        	]
        pocitadlo_cyklu_programu = 0
        copy_grid(grid0, grid_default)
    if y_pos == 11 and (x_pos == 3 or x_pos == 4 or x_pos == 5):
        varianta_sudoku = "killer"
        grid0 =[
        		[0, 4, 5, 0, 0, 0, 3, 0, 0],
        		[0, 0, 0, 0, 0, 8, 0, 0, 6],
        		[8, 0, 0, 0, 0, 6, 0, 0, 4],
        		[0, 9, 7, 0, 6, 0, 0, 0, 0],
        		[0, 0, 0, 2, 0, 1, 0, 0, 0],
        		[0, 0, 0, 0, 5, 0, 8, 4, 0],
        		[5, 0, 0, 9, 0, 0, 0, 0, 8],
        		[7, 0, 0, 6, 0, 0, 0, 0, 0],
        		[0, 0, 4, 0, 0, 0, 6, 7, 0]
        	]
        pocitadlo_cyklu_programu = 0
        copy_grid(grid0, grid_default)
    if y_pos == 11 and (x_pos == 6 or x_pos == 7 or x_pos == 8):
        varianta_sudoku = "windoku"
        grid0 =[
        		[0, 0, 0, 4, 0, 9, 0, 0, 0],
        		[0, 9, 3, 0, 0, 0, 7, 0, 0],
        		[0, 0, 0, 0, 0, 0, 9, 2, 0],
        		[1, 0, 0, 0, 0, 4, 0, 0, 6],
        		[0, 0, 0, 3, 0, 0, 0, 0, 0],
        		[9, 0, 0, 0, 1, 0, 0, 0, 8],
        		[0, 0, 8, 0, 0, 0, 0, 9, 0],
        		[0, 6, 0, 0, 0, 0, 0, 8, 0],
        		[2, 0, 0, 1, 0, 5, 0, 0, 0]
        	]
        pocitadlo_cyklu_programu = 0
        copy_grid(grid0, grid_default)
    
    
    
    if ukazatel_pozice_na_obrazovce == 1:
        draw_box()

    
    pg.display.flip()
        
pg.quit()