# import simplex solver classes
from simplex_alg import *

# intialize cargo problem and add constraints
cargo = simplex_two_phase()
cargo.get_obj_fxn('max 280tf1+280tm1+280tb1+360tf2+360tm2+360tb2+320tf3+320tm3+320tb3+250tf4+250tm4+250tb4')
cargo.add_constraints('1tf1+1tf2+1tf3+1tf4 <= 12')
cargo.add_constraints('1tm1+1tm2+1tm3+1tm4 <= 18')
cargo.add_constraints('1tb1+1tb2+1tb3+1tb4 <= 10')
cargo.add_constraints('500tf1+700tf2+600tf3+400tf4 <= 7000')
cargo.add_constraints('500tm1+700tm2+600tm3+400tm4 <= 9000')
cargo.add_constraints('500tb1+700tb2+600tb3+400tb4 <= 5000')
cargo.add_constraints('1tf1+1tm1+1tb1 <= 20')
cargo.add_constraints('1tf2+1tm2+1tb2 <= 16')
cargo.add_constraints('1tf3+1tm3+1tb3 <= 25')
cargo.add_constraints('1tf4+1tm4+1tb4 <= 13')
cargo.add_constraints('10tf1+10tf2+10tf3+10tf4-3tf1-3tf2-3tf3-3tf4-3tm1-3tm2-3tm3-3tm4-3tb1-3tb2-3tb3-3tb4 <= 0')
cargo.add_constraints('20tm1+20tm2+20tm3+20tm4-9tf1-9tf2-9tf3-9tf4-9tm1-9tm2-9tm3-9tm4-9tb1-9tb2-9tb3-9tb4 <= 0')
cargo.add_constraints('10tb1+10tb2+10tb3+10tb4-1tf1-1tf2-1tf3-1tf4-1tm1-1tm2-1tm3-1tm4-1tb1-1tb2-1tb3-1tb4 <= 0')
cargo.add_constraints('10tf1+10tf2+10tf3+10tf4-3tf1-3tf2-3tf3-3tf4-3tm1-3tm2-3tm3-3tm4-3tb1-3tb2-3tb3-3tb4 >= 0')
cargo.add_constraints('20tm1+20tm2+20tm3+20tm4-9tf1-9tf2-9tf3-9tf4-9tm1-9tm2-9tm3-9tm4-9tb1-9tb2-9tb3-9tb4 >= 0')
cargo.add_constraints('10tb1+10tb2+10tb3+10tb4-1tf1-1tf2-1tf3-1tf4-1tm1-1tm2-1tm3-1tm4-1tb1-1tb2-1tb3-1tb4 >= 0')

# solve problem
cargo.simplex()

# initialize radio problem and constraints
radio = simplex_two_phase()
radio.get_obj_fxn('max 15r1+13r2+11r3+9r4-200wr1-200wt1-200wr2-200wt2-200wr3-200wt3-200wr4-200wt4-100t1-100t2-100t3')
radio.add_constraints('1r1-50wr1 <= 0')
radio.add_constraints('1r2-50wr2 <= 0')
radio.add_constraints('1r3-50wr3 <= 0')
radio.add_constraints('1r4-50wr4 <= 0')
radio.add_constraints('1wr1+1wt1 <= 40')
radio.add_constraints('1wr2+1wt2-1wr1-4wt1 <= 0')
radio.add_constraints('1wr3+1wt3-1wr2-4wt2 <= 0')
radio.add_constraints('1wr4+1wt4-1wr3-4wt3 <= 0')
radio.add_constraints('1r1+1r2+1r3+1r4 <= 21475')
radio.add_constraints('1t1-3wt1 <= 0')
radio.add_constraints('1t2-3wt2 <= 0')
radio.add_constraints('1t3-3wt3 <= 0')
radio.add_constraints('1r1-50wr1 >= 0')
radio.add_constraints('1r2-50wr2 >= 0')
radio.add_constraints('1r3-50wr3 >= 0')
radio.add_constraints('1r4-50wr4 >= 0')
radio.add_constraints('1wr1+1wt1 >= 40')
radio.add_constraints('1wr2+1wt2-1wr1-4wt1 >= 0')
radio.add_constraints('1wr3+1wt3-1wr2-4wt2 >= 0')
radio.add_constraints('1wr4+1wt4-1wr3-4wt3 >= 0')
radio.add_constraints('1r1+1r2+1r3+1r4 = 21475')
radio.add_constraints('1t1-3wt1 >= 0')
radio.add_constraints('1t2-3wt2 >= 0')
radio.add_constraints('1t3-3wt3 >= 0')

# solve problem
radio.simplex()