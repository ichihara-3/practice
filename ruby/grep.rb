# ruby grep


module Grep 
  def grep
    File.open(filename, 'r') do |f|
      f.each_line do |line|
        if string.match(line)
          puts "l.#{f.lineno} #{line}"
        end
      end
    end
  end
end

class RubyGrep
  include Grep 
  attr_accessor :string, :filename

  def initialize(string, filename)
    @string = string
    @filename = filename
  end

  def string
    Regexp.new(@string)
  end

  def filename
    @filename
  end
end


g = RubyGrep.new(ARGV[0], ARGV[1])
g.grep
