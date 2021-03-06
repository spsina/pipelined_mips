from alu import ALU
from decs import WORD


class RegisterFile:

    def __init__(self, register_size=WORD, count=32):
        self.register_size = WORD
        self.count = count
        self.data = {}

        # initialize registers
        for i in range(self.count):
            self.data[ALU.int_to_n_bit_binary(i, 5)] = ALU.int_to_n_bit_binary(0, register_size)

        # read registers
        self._read_r1 = ALU.int_to_n_bit_binary(0, 5)
        self._read_r2 = ALU.int_to_n_bit_binary(0, 5)

        # register read data
        self.read_d1 = ALU.int_to_n_bit_binary(0)
        self.read_d2 = ALU.int_to_n_bit_binary(0)

        # write enable and write register write data
        self._reg_write = False
        self._write_r = ALU.int_to_n_bit_binary(0, 5)
        self._write_data = ALU.int_to_n_bit_binary(0)

    def _exc(self):

        """
            to avoid structural hazard
            first writing will happen
            then reading
        """

        # first do the writing
        self.write()

        # the do the reads
        self.read_data_x(1)
        self.read_data_x(2)

    def validate_register(self, register):
        """

        :param register: validate the given register by type, length, and existence
        :return:
        """

        if not (type(register) == tuple and
                register in self.data.keys()):
            raise Exception("Invalid register")

    def validate_data(self, data):
        """
        :param data: validate by type and length
        :return:
        """

        if not (type(data) == tuple and len(data) == self.register_size):
            raise Exception("Invalid register data")

    def at(self, register):
        """

        :param register:
        :return: content of the given register
        """
        self.validate_register(register)
        return self.data[register]

    def put(self, register, data):
        """

        :param register:
        :param data:
        :return:
        """

        self.validate_register(register)
        self.validate_data(data)

        self.data[register] = data

    def set_read_r1(self, register):
        self.validate_register(register)
        self._read_r1 = register

        self._exc()

    def set_read_r2(self, register):
        self.validate_register(register)
        self._read_r2 = register

        self._exc()

    def set_write_r(self, register):
        self.validate_register(register)
        self._write_r = register

        self._exc()

    def set_write_data(self, data):
        self.validate_data(data)
        self._write_data = data

        self._exc()

    def set_register_write(self, reg_write):
        self._reg_write = reg_write

        self._exc()

    def read_data_x(self, x):
        """
        set read_x by content at read_x
        :return: data at read_x
        """

        if x == 1:
            read_addr = self._read_r1
        else:
            read_addr = self._read_r2

        data = self.at(read_addr)

        if x == 1:
            self.read_d1 = data
        else:
            self.read_d2 = data

        return data

    def write(self):
        if self._reg_write:
            self.put(self._write_r, self._write_data)
