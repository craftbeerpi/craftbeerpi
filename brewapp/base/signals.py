from blinker import Namespace
brew_signals = Namespace()

next_step = brew_signals.signal('next_step')
reset_step = brew_signals.signal('reset_step')
start_brew = brew_signals.signal('start_brew')
start_timer = brew_signals.signal('start_timer')
