#pragma once

#include "visitor.h"
#include <any>
#include <stdexcept>

struct calculator : visitor {
    std::any visit_num(num_node *node) override {
        return node->number;
    }

    std::any visit_add(add_node *node) override {
        std::any left = visit(node->lnode);
        std::any right = visit(node->rnode);
        if (left.type() == typeid(long long) && right.type() == typeid(long long)) {
            return std::any_cast<long long>(left) + std::any_cast<long long>(right);
        } else if (left.type() == typeid(double) && right.type() == typeid(double)) {
            return std::any_cast<double>(left) + std::any_cast<double>(right);
        }
        throw std::runtime_error("Type mismatch or unsupported type in add");
    }

    std::any visit_sub(sub_node *node) override {
        std::any left = visit(node->lnode);
        std::any right = visit(node->rnode);
        if (left.type() == typeid(long long) && right.type() == typeid(long long)) {
            return std::any_cast<long long>(left) - std::any_cast<long long>(right);
        } else if (left.type() == typeid(double) && right.type() == typeid(double)) {
            return std::any_cast<double>(left) - std::any_cast<double>(right);
        }
        throw std::runtime_error("Type mismatch or unsupported type in sub");
    }

    std::any visit_mul(mul_node *node) override {
        std::any left = visit(node->lnode);
        std::any right = visit(node->rnode);
        if (left.type() == typeid(long long) && right.type() == typeid(long long)) {
            return std::any_cast<long long>(left) * std::any_cast<long long>(right);
        } else if (left.type() == typeid(double) && right.type() == typeid(double)) {
            return std::any_cast<double>(left) * std::any_cast<double>(right);
        }
        throw std::runtime_error("Type mismatch or unsupported type in mul");
    }

    std::any visit_div(div_node *node) override {
        std::any left = visit(node->lnode);
        std::any right = visit(node->rnode);
        if (left.type() == typeid(long long) && right.type() == typeid(long long)) {
            return std::any_cast<long long>(left) / std::any_cast<long long>(right);
        } else if (left.type() == typeid(double) && right.type() == typeid(double)) {
            return std::any_cast<double>(left) / std::any_cast<double>(right);
        }
        throw std::runtime_error("Type mismatch or unsupported type in div");
    }

    ~calculator() override = default;
};
