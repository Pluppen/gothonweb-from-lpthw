from nose.tools import *
from app import app

app.config['TESTING'] = True
web = app.test_client()

@nottest
def input_test(action, expect):
  data = {'action': action}
  rv = web.post('/game', follow_redirects=True, data=data)
  assert_in(bytes(expect, encoding='utf-8'), rv.data)

@nottest
def start_game():
  rv = web.get("/", follow_redirects=True)
  assert_equal(rv.status_code, 200)
  assert_in(b"Central Corridor", rv.data)

def test_index():
  rv = web.get('/random', follow_redirects=True)
  assert_equal(rv.status_code, 404)

  rv = web.get('/', follow_redirects=True)
  assert_equal(rv.status_code, 200)

def win_test():
  start_game()

  input_test('tell a joke', 'Laser Weapon Armory')

  input_test('0132', 'The Bridge')

  input_test('slowly place the bomb', 'Escape Pod')

  input_test('2', 'The End')

def death_central_corridor():
  start_game()

  input_test('shoot!', 'Death')

def death_laswer_weapon_armory():
  start_game()

  input_test('tell a joke', 'Laser Weapon Armory')

  input_test('0345', 'Death')

def death_the_bridge():
  start_game()

  input_test('tell a joke', 'Laser Weapon Armory')

  input_test('0132', 'The Bridge')

  input_test('throw the bomb!', 'Death')

def death_escape_pod():
  start_game()

  input_test('tell a joke', 'Laser Weapon Armory')

  input_test('0132', 'The Bridge')

  input_test('slowly place the bomb', 'Escape pod')

  input_test('1', 'The End')