# Crystal

### Basic Setup
```
set PROJNAME crystal_day01
crystal init app $PROJNAME
rm -rf $PROJNAME/.git
cd $PROJNAME
nvim src/$PROJNAME.cr src/main.cr spec/{$PROJNAME}_spec.cr -p
```

### `src/crystal_day01.cr`
```crystal
# TODO: Write documentation for `CrystalDay01`
module CrystalDay01
  VERSION = "0.1.0"

  # TODO: Put your code here
  def self.add_one(x)
    x + 1
  end
end
```

### `src/main.cr`
```crystal
require "./crystal_day01"
puts "hello"
puts CrystalDay01.add_one(100)
```

### `spec/crystal_day01_spec.cr`
```crystal
require "./spec_helper"

describe CrystalDay01 do
  # TODO: Write tests

  it "works" do
    CrystalDay01.add_one(500).should eq (501)
  end
end
```

### `./Makefile` (requires tabs!)
```
run:
        crystal run src/main.cr
test:
        crystal spec
format:
        crystal tool format
repl:
        crystal play --binding 0.0.0.0
```

