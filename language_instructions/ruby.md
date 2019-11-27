# Ruby

## Basic Setup

```fish
set PROJNAME ruby_day01
set FILENAME day01
mkdir $PROJNAME
cd $PROJNAME
bundler init
bundler add rspec prettier require_all
bundle install --binstubs
echo "bin" >> .gitignore
bin/rspec --init
mkdir lib
touch main.rb
chmod +x main.rb
nvim lib/{$FILENAME}.rb main.rb spec/{$FILENAME}_spec.rb Makefile -p
```

## `./lib/day01.rb`

```ruby
class Day01
  def self.testme()
    500
  end
end
```

## `./spec/day01_spec.rb`

```ruby
require 'day01'

RSpec.describe Day01, 'testme' do
  context 'whatever' do
    it 'returns 500' do
      got = Day01.testme
      expect(got).to eq 500
    end
  end
end
```

## `./main.rb`

```ruby
#!/usr/bin/env ruby
require 'require_all'
require_all './lib'

puts Day01.testme
```

## `./Makefile` (requires tabs!)

```makefile
run:
        ./main.rb
test:
        ./bin/rspec
repl:
        irb
format:
        bundle exec rbprettier --write '**/*.rb'
```
