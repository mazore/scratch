from blocks.action.move_block import MoveBlock
from blocks.action.print_block import PrintBlock
from blocks.action.wait_block import WaitBlock
from blocks.action.restart_block import RestartBlock

from blocks.control.forever_block import ForeverBlock
from blocks.control.if_block import IfBlock

from blocks.event.on_run_block import OnRunBlock
from blocks.event.on_click_block import OnClickBlock

from blocks.operator.math_blocks import AddBlock, SubtractBlock, MultiplyBlock, DivideBlock
from blocks.operator.math_blocks import ModulusBlock, GreaterThanBlock, LessThanBlock, EqualToBlock
from blocks.operator.math_blocks import AndBlock, OrBlock
from blocks.operator.not_block import NotBlock
from blocks.operator.random_block import RandomBlock
from blocks.operator.touching_block import TouchingBlock

from blocks.variable.mouse_pos_blocks import MouseXBlock, MouseYBlock
from blocks.variable.change_block import ChangeBlock
from blocks.variable.get_block import GetBlock
from blocks.variable.set_block import SetBlock

block_types = [
    OnRunBlock,
    OnClickBlock,

    MoveBlock,
    PrintBlock,
    RestartBlock,
    WaitBlock,

    ForeverBlock,
    IfBlock,

    AddBlock,
    AndBlock,
    DivideBlock,
    EqualToBlock,
    GreaterThanBlock,
    LessThanBlock,
    ModulusBlock,
    MultiplyBlock,
    NotBlock,
    OrBlock,
    RandomBlock,
    SubtractBlock,
    TouchingBlock,

    ChangeBlock,
    SetBlock,
    MouseXBlock,
    MouseYBlock,
    GetBlock,
]
