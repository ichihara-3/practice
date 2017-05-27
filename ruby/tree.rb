# tree module


class Tree
  attr_accessor :children, :node_name

  def initialize(tree)
      tree.each do |parent, children|
        @children = self.children_node(children) 
        @node_name = parent
      end
  end

  def children_node(children)
    c = []
    unless children.is_a?(Array)
      children.each do |key, value|
        c.push(Tree.new({key => value}))
      end
    end
    c
  end


  def visit_all(&block)
    visit &block
    children.each {|c| c.visit_all &block}
  end

  def visit (&block)
    block.call self
  end
end

ruby_tree = Tree.new({
    'grandpa' => { 
        'dad' => {
            'child 1' => [],
            'child 2' => []}}})

puts "Visiting a node"
ruby_tree.visit {|node| puts node.node_name}
puts

puts "visiting entire tree"
ruby_tree.visit_all {|node| puts node.node_name}
