# Ruby

### Basic Setup
```
set PROJNAME ruby_day01
mkdir $PROJNAME
cd $PROJNAME
bundler init
bundler add rspec prettier require_all
bundle install --binstubs
echo "bin" >> .gitignore
bin/rspec --init
mkdir lib
nvim lib/day01.rb
nvim main.rb
nvim spec/day01_spec.rb
nvim Makefile
chmod +x main.rb
```

### `./lib/day01.rb`
```ruby
class Day01
  def self.testme()
    500
  end
end
```

### `./spec/day01_spec.rb`
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

### `./main.rb`
```
#!/usr/bin/env ruby
require 'require_all'
require_all './lib'

puts Day01.testme
```

### `./Makefile` (requires tabs!)
```
run:
        ./main.rb
test:
        ./bin/rspec
```
